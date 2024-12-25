import { items } from "@/constants/items";
import { PredictResult } from "@/model/predict";
import ItemProvider, { useItem } from "@/providers/item";
import { usePrediction } from "@/providers/prediction";
import { Button } from "@/ui/button";
import { FC, memo } from "react";
import ItemImage from "./item-image";

interface ItemProps {
  result: PredictResult;
}

const PredictResultItem: FC<ItemProps> = memo((props) => {
  const { result } = props;
  const item = items[result.id];
  const { openModal } = useItem();
  return (
    <Button
      unstyled
      className="flex min-w-24 max-w-32 flex-col items-center rounded bg-neutral-900/80 px-3 py-2 text-center text-white"
      onClick={() => openModal(result.id)}
    >
      <ItemImage itemId={item.id} />
      <div className="flex h-full flex-col items-center justify-center">
        <p className="mt-1 text-sm font-bold">{item?.name || "Not found"}</p>
        <p className="font-medium">{result.probability + "%"}</p>
      </div>
    </Button>
  );
});

const PredictResultsList: FC = () => {
  const { results } = usePrediction();
  if (!results) return null;
  if (results.length === 0) return null;
  return (
    <ItemProvider>
      <div className="no-scrollbar absolute bottom-20 z-20 flex w-10/12 gap-2 overflow-scroll">
        {results.map((result) => (
          <PredictResultItem key={result.id} result={result} />
        ))}
      </div>
    </ItemProvider>
  );
};

export default PredictResultsList;
