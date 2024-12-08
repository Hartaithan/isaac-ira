import { useCamera } from "@/providers/camera";
import { Button } from "@/ui/button";
import { FC } from "react";

const CaptureButton: FC = () => {
  const { capture } = useCamera();
  return (
    <Button className="absolute bottom-6 z-20" onClick={capture}>
      Capture
    </Button>
  );
};

export default CaptureButton;
