import { FC } from "react";
import Camera from "./components/camera";
import CaptureButton from "./components/capture-button";
import CenterPoint from "./components/center-point";
import RootProvider from "./providers/root";

const App: FC = () => (
  <RootProvider>
    <Camera />
    <CaptureButton />
    <CenterPoint />
  </RootProvider>
);

export default App;
