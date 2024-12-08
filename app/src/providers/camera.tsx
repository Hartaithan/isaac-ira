import { center } from "@/constants/dimensions";
import { resizeCanvas } from "@/utils/canvas";
import { predict } from "@/utils/model";
import {
  createContext,
  FC,
  PropsWithChildren,
  RefObject,
  useCallback,
  useContext,
  useMemo,
  useRef,
} from "react";

interface Context {
  camera: RefObject<HTMLVideoElement>;
  initialize: () => void;
  stop: () => void;
  capture: () => void;
}

const initialValue: Context = {
  camera: { current: null },
  initialize: () => null,
  stop: () => null,
  capture: () => null,
};

const constraints: MediaStreamConstraints = {
  video: { facingMode: "environment" },
};

const Context = createContext<Context>(initialValue);

const CameraProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  const camera = useRef<HTMLVideoElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const cropped = useRef<HTMLCanvasElement>(null);

  const initialize: Context["initialize"] = useCallback(async () => {
    try {
      if (!camera.current) return;
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      camera.current.srcObject = stream;
      await camera.current.play();
    } catch (error) {
      console.error("initialize camera error", error);
    }
  }, []);

  const stop: Context["stop"] = useCallback(() => {
    if (!camera.current || !camera.current.srcObject) return;
    const stream = camera.current.srcObject as MediaStream;
    const tracks = stream.getTracks();
    tracks.forEach((track) => track.stop());
  }, []);

  const capture: Context["capture"] = useCallback(async () => {
    if (!camera.current) return;
    if (!canvas.current) return;
    if (!cropped.current) return;

    const { videoHeight, videoWidth } = camera.current;

    const context = canvas.current.getContext("2d");
    if (!context) return;

    canvas.current.width = videoWidth;
    canvas.current.height = videoHeight;
    context.drawImage(camera.current, 0, 0, videoWidth, videoHeight);

    const x = (videoWidth - center.width) / 2;
    const y = (videoHeight - center.height) / 2;

    const croppedData = context.getImageData(x, y, center.width, center.height);
    cropped.current.width = center.width;
    cropped.current.height = center.height;

    const croppedContext = cropped.current.getContext("2d");
    if (!croppedContext) return;
    croppedContext.putImageData(croppedData, 0, 0);

    const resized = resizeCanvas(cropped.current);
    if (!resized) return;
    const result = predict(resized);
    console.info("result", result);
  }, []);

  const exposed: Context = useMemo(
    () => ({ camera, initialize, stop, capture }),
    [initialize, stop, capture],
  );

  return (
    <Context.Provider value={exposed}>
      {children}
      <canvas className="absolute hidden" ref={canvas} />
      <canvas className="absolute z-10" ref={cropped} />
    </Context.Provider>
  );
};

export const useCamera = (): Context => useContext(Context);

export default CameraProvider;
