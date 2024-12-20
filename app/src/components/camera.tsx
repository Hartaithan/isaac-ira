import { useCamera } from "@/providers/camera";
import { FC, useEffect } from "react";

const Camera: FC = () => {
  const { camera, initialize, stop } = useCamera();

  useEffect(() => {
    initialize();
    return () => stop();
  }, [initialize, stop]);

  return (
    <div className="flex size-full items-center justify-center overflow-hidden">
      <video ref={camera} className="hidden size-full object-cover" />
    </div>
  );
};

export default Camera;
