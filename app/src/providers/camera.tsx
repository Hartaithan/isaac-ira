import { center } from "@/constants/dimensions";
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
  video: RefObject<HTMLVideoElement>;
  initialize: () => void;
  stop: () => void;
  capture: () => void;
}

const initialValue: Context = {
  video: { current: null },
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
  const video = useRef<HTMLVideoElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const cropped = useRef<HTMLCanvasElement>(null);

  const initialize: Context["initialize"] = useCallback(async () => {
    try {
      if (!video.current) return;
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      video.current.srcObject = stream;
      await video.current.play();
    } catch (error) {
      console.error("initialize camera error", error);
    }
  }, []);

  const stop: Context["stop"] = useCallback(() => {
    if (!video.current || !video.current.srcObject) return;
    const stream = video.current.srcObject as MediaStream;
    const tracks = stream.getTracks();
    tracks.forEach((track) => track.stop());
  }, []);

  const capture: Context["capture"] = useCallback(() => {
    if (!video.current) return;
    if (!canvas.current) return;
    if (!cropped.current) return;

    const { videoHeight, videoWidth } = video.current;

    const context = canvas.current.getContext("2d");
    if (!context) return;

    canvas.current.width = videoWidth;
    canvas.current.height = videoHeight;
    context.drawImage(video.current, 0, 0, videoWidth, videoHeight);

    const x = (videoWidth - center.width) / 2;
    const y = (videoHeight - center.height) / 2;

    const croppedData = context.getImageData(x, y, center.width, center.height);
    cropped.current.width = center.width;
    cropped.current.height = center.height;

    const croppedContext = cropped.current.getContext("2d");
    if (!croppedContext) return;

    croppedContext.putImageData(croppedData, 0, 0);
    const croppedImage = cropped.current.toDataURL("image/png");
    console.info("croppedImage", croppedImage);
  }, []);

  const exposed: Context = useMemo(
    () => ({ video, initialize, stop, capture }),
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
