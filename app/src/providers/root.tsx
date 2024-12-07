import { FC, PropsWithChildren } from "react";
import CameraProvider from "./camera";

const RootProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  return <CameraProvider>{children}</CameraProvider>;
};

export default RootProvider;
