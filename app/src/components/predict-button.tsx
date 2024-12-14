import { useCamera } from "@/providers/camera";
import { Button } from "@/ui/button";
import { predict } from "@/utils/model";
import { FC, useCallback } from "react";

const PredictButton: FC = () => {
  const { capture } = useCamera();

  const handlePredict = useCallback(async () => {
    const canvas = capture();
    if (!canvas) return;
    const predictResults = await predict(canvas);
    if (predictResults) {
      console.info("predictResults", predictResults);
    } else {
      console.error("predict results not found");
    }
  }, [capture]);

  return <Button onClick={handlePredict}>Predict</Button>;
};

export default PredictButton;
