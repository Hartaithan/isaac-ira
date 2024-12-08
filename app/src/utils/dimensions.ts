import { Dimensions } from "@/model/dimension";
import { RefObject } from "react";

export const getVideoSize = (video: RefObject<HTMLVideoElement>) => {
  const width = video.current?.videoWidth || 0;
  const height = video.current?.videoHeight || 0;
  return { width, height };
};

export const getActualSize = (
  viewport: Dimensions,
  camera: Dimensions,
): Dimensions => {
  const screenRatio = viewport.width / viewport.height;
  const cameraRatio = camera.width / camera.height;
  if (screenRatio > cameraRatio) {
    const width = viewport.width;
    const height = Math.round(viewport.width / cameraRatio);
    return { width, height };
  } else {
    const width = Math.round(viewport.height * cameraRatio);
    const height = viewport.height;
    return { width, height };
  }
};

export const getRatio = (viewport: Dimensions, camera: Dimensions): number => {
  return viewport.width / camera.width;
};
