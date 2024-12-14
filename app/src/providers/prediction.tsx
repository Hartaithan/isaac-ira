import { PredictResult } from "@/model/predict";
import { predict } from "@/utils/model";
import {
  createContext,
  FC,
  PropsWithChildren,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";

type PredictionHandler = (canvas: HTMLCanvasElement) => Promise<void>;

interface Context {
  results: PredictResult[] | null;
  makePrediction: PredictionHandler;
}

const initialValue: Context = {
  results: null,
  makePrediction: async () => {},
};

const Context = createContext<Context>(initialValue);

const PredictionProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  const [results, setResults] = useState<Context["results"]>(
    initialValue.results,
  );

  const makePrediction: Context["makePrediction"] = useCallback(
    async (canvas) => {
      const predictResults = await predict(canvas);
      if (predictResults) {
        setResults(predictResults);
      } else {
        console.error("predict results not found");
      }
    },
    [],
  );

  const exposed: Context = useMemo(
    () => ({ results, makePrediction }),
    [makePrediction, results],
  );

  return <Context.Provider value={exposed}>{children}</Context.Provider>;
};

export const usePrediction = (): Context => useContext(Context);

export default PredictionProvider;
