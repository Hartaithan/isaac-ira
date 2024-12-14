import { classes } from "@/constants/classes";
import { PredictResult } from "@/model/predict";
import * as tf from "@tensorflow/tfjs";

export const loadModel = async () => {
  try {
    return await tf.loadLayersModel("model/model.json");
  } catch (error) {
    console.error("load model error", error);
    return null;
  }
};

const formatPredictResults = (values: number[]) => {
  const results: PredictResult[] = [];
  for (let index = 0; index < values.length; index++) {
    const result = values[index];
    const probability = Number((result * 100).toFixed(2));
    results.push({ id: classes[index], probability });
  }
  return results;
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
    const values = Array.from(predictions.dataSync());
    const formatted = formatPredictResults(values);
    const results = formatted
      .sort((a, b) => b.probability - a.probability)
      .slice(0, 10);
    return results;
  } catch (error) {
    console.error("predict error", error);
    return null;
  }
};
