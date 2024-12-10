import * as tf from "@tensorflow/tfjs";

export const loadModel = async () => {
  try {
    return await tf.loadLayersModel("model/model.json");
  } catch (error) {
    console.error("load model error", error);
    return null;
  }
};

export const predict = async (canvas: HTMLCanvasElement) => {
  try {
    const model = await loadModel();
    if (!model) throw new Error("model not found");
    const tensor = tf.browser
      .fromPixels(canvas)
      .resizeBilinear([224, 224])
      .toFloat()
      .expandDims();
    const predictions = model.predict(tensor) as tf.Tensor;
    const result = predictions.argMax(-1).dataSync()[0];
    return result;
  } catch (error) {
    console.error("predict error", error);
    return null;
  }
};
