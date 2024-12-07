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
}

const initialValue: Context = {
  video: { current: null },
  initialize: () => null,
  stop: () => null,
};

const constraints: MediaStreamConstraints = {
  video: { facingMode: "environment" },
};

const Context = createContext<Context>(initialValue);

const CameraProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  const video = useRef<HTMLVideoElement>(null);

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

  const exposed: Context = useMemo(
    () => ({ video, initialize, stop }),
    [initialize, stop],
  );

  return <Context.Provider value={exposed}>{children}</Context.Provider>;
};

export const useCamera = (): Context => useContext(Context);

export default CameraProvider;
