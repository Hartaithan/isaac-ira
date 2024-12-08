import { center } from "@/constants/dimensions";
import { useViewportSize } from "@/hooks/useViewportSize";
import { Dimensions } from "@/model/dimension";
import { useCamera } from "@/providers/camera";
import { getActualSize, getRatio, getVideoSize } from "@/utils/dimensions";
import { FC, useMemo } from "react";

const CenterPoint: FC = () => {
  const { video } = useCamera();
  const viewportSize = useViewportSize();

  const centerSize = useMemo(() => {
    const cameraSize = getVideoSize(video);
    const actualCameraSize = getActualSize(viewportSize, cameraSize);
    const viewportToCameraRatio = getRatio(actualCameraSize, cameraSize);
    const actualCenterSize: Dimensions = {
      width: center.width * viewportToCameraRatio || center.width,
      height: center.height * viewportToCameraRatio || center.height,
    };
    return actualCenterSize;
  }, [video, viewportSize]);

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
