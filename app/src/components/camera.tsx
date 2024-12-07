import { useCamera } from "@/providers/camera";
import { FC, useEffect } from "react";

const Camera: FC = () => {
  const { video, initialize, stop } = useCamera();

  useEffect(() => {
    initialize();
    return () => stop();
  }, [initialize, stop]);

  return (
    <div className="size-full overflow-hidden flex justify-center items-center">
      <video ref={video} className="size-full object-cover" />
    </div>
  );
};

export default Camera;
