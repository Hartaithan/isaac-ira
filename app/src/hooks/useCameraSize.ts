import { Dimensions } from "@/model/dimension";
import { getVideoSize } from "@/utils/dimensions";
import { RefObject, useEffect, useState } from "react";

export const useCameraSize = (video: RefObject<HTMLVideoElement>) => {
  const [size, setSize] = useState<Dimensions>({ width: 0, height: 0 });

  useEffect(() => {
    const element = video.current;
    if (!element) return;

    const handleMetadata = () => {
      const videoSize = getVideoSize(video);
      setSize(videoSize);
    };

    element.addEventListener("loadedmetadata", handleMetadata);
    return () => element.removeEventListener("loadedmetadata", handleMetadata);
  }, [video]);

  return size;
};
