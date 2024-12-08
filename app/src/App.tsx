import { FC } from "react";
import Camera from "./components/camera";
import CaptureButton from "./components/capture-button";
import RootProvider from "./providers/root";

const App: FC = () => (
  <RootProvider>
    <Camera />
    <CaptureButton />
  </RootProvider>
);

export default App;
