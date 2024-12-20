import { Item } from "@/model/item";
import { CSSProperties } from "react";

export const getItemStyles = (item: Item): CSSProperties => {
  const { image_url, position, width, height } = item;
  const [x, y] = position;
  return {
    backgroundImage: `url(./images/${image_url.replace(".png", ".avif")})`,
    backgroundPositionX: `-${x}px`,
    backgroundPositionY: `${y}px`,
    backgroundRepeat: "no-repeat",
    width,
    height,
  };
};
