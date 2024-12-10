export const resizeCanvas = (
  canvas: HTMLCanvasElement,
  width = 224,
  height = 224,
) => {
  const resized = document.createElement("canvas");
  const ctx = resized.getContext("2d");
  if (!ctx) return null;
  resized.width = width;
  resized.height = height;
  ctx.drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, 224, 224);
  return resized;
};
