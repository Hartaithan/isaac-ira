import { Item } from "@/model/item";
import { CSSProperties } from "react";

export const getItemStyles = (item: Item): CSSProperties => {
  const { image_url, position, width, height } = item;
  return {
    backgroundImage: `url(./images/${image_url.replace(".png", ".avif")})`,
    backgroundPositionX: `-${position[0]}px`,
    backgroundPositionY: `${position[1]}px`,
    backgroundRepeat: "no-repeat",
    width,
    height,
  };
};
