import { center } from "@/constants/dimensions";
import { useCameraSize } from "@/hooks/useCameraSize";
import { useViewportSize } from "@/hooks/useViewportSize";
import { Dimensions } from "@/model/dimension";
import { useCamera } from "@/providers/camera";
import { getActualSize, getRatio } from "@/utils/dimensions";
import { FC, useMemo } from "react";

const CenterPoint: FC = () => {
  const { camera } = useCamera();
  const viewportSize = useViewportSize();
  const cameraSize = useCameraSize(camera);

  const centerSize = useMemo(() => {
    const actualCameraSize = getActualSize(viewportSize, cameraSize);
    const viewportToCameraRatio = getRatio(actualCameraSize, cameraSize);
    const actualCenterSize: Dimensions = {
      width: center.width * viewportToCameraRatio || center.width,
      height: center.height * viewportToCameraRatio || center.height,
    };
    return actualCenterSize;
  }, [cameraSize, viewportSize]);

  return (
    <div
      className="absolute flex items-center justify-center border-2 border-dashed text-white"
      style={centerSize}
    >
      +
    </div>
  );
};

export default CenterPoint;
