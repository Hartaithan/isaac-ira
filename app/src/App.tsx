import { FC } from "react";
import Camera from "./components/camera";
import CaptureButton from "./components/capture-button";
import CenterPoint from "./components/center-point";
import PredictButton from "./components/predict-button";
import RootProvider from "./providers/root";

const App: FC = () => (
  <RootProvider>
    <Camera />
    <CenterPoint />
    <div className="absolute bottom-6 z-20 flex gap-x-3">
      <CaptureButton />
      <PredictButton />
    </div>
  </RootProvider>
);

export default App;
