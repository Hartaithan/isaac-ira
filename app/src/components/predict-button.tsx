import { useCamera } from "@/providers/camera";
import { usePrediction } from "@/providers/prediction";
import { Button } from "@/ui/button";
import { FC, useCallback } from "react";

const PredictButton: FC = () => {
  const { capture } = useCamera();
  const { makePrediction } = usePrediction();

  const handlePredict = useCallback(() => {
    const canvas = capture();
    if (!canvas) return;
    makePrediction(canvas);
  }, [capture, makePrediction]);

  return <Button onClick={handlePredict}>Predict</Button>;
};

export default PredictButton;
