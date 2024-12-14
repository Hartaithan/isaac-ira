import { FC, PropsWithChildren } from "react";
import CameraProvider from "./camera";
import PredictionProvider from "./prediction";

const RootProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  return (
    <CameraProvider>
      <PredictionProvider>{children}</PredictionProvider>
    </CameraProvider>
  );
};

export default RootProvider;
