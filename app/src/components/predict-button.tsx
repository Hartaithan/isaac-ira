import { classes } from "@/constants/classes";
import { useCamera } from "@/providers/camera";
import { Button } from "@/ui/button";
import { predict } from "@/utils/model";
import { FC, useCallback } from "react";

const PredictButton: FC = () => {
  const { capture } = useCamera();

  const handlePredict = useCallback(async () => {
    const canvas = capture();
    if (!canvas) return;
    const result = await predict(canvas);
    alert(result !== null ? classes[result] : "not found");
  }, [capture]);

  return <Button onClick={handlePredict}>Predict</Button>;
};

export default PredictButton;
