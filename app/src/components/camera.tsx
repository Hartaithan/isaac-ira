import { useCamera } from "@/providers/camera";
import { Button } from "@/ui/button";
import { FC, useEffect } from "react";

const Camera: FC = () => {
  const { video, initialize, stop, capture } = useCamera();

  useEffect(() => {
    initialize();
    return () => stop();
  }, [initialize, stop]);

  return (
    <div className="flex size-full items-center justify-center overflow-hidden">
      <video ref={video} className="size-full object-cover" />
      <Button className="absolute bottom-6 z-20" onClick={capture}>
        Capture
      </Button>
    </div>
  );
};

export default Camera;
