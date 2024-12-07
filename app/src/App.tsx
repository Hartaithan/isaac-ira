import { FC } from "react";
import Camera from "./components/camera";
import RootProvider from "./providers/root";

const App: FC = () => (
  <RootProvider>
    <Camera />
  </RootProvider>
);

export default App;
