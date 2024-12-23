import { items } from "@/constants/items";
import { Item } from "@/model/item";
import { PredictResult } from "@/model/predict";
import { usePrediction } from "@/providers/prediction";
import { getItemStyles } from "@/utils/item";
import { FC, memo } from "react";

interface ItemProps {
  result: PredictResult;
}

interface ItemImageProps {
  size?: number;
  item: Item;
}

const ItemImage: FC<ItemImageProps> = (props) => {
  const { item } = props;
  return (
    <img
      src="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
      style={getItemStyles(item)}
      alt={item.name + " " + item.description}
    />
  );
};

const PredictResultItem: FC<ItemProps> = memo((props) => {
  const { result } = props;
  const item = items[result.id];
  return (
    <div className="flex min-w-24 flex-col items-center rounded bg-neutral-900/80 px-3 py-2 text-center text-white">
      <ItemImage item={item} />
      <p className="mt-1 text-sm font-bold">{item?.name || "Not found"}</p>
      <p className="font-medium">{result.probability + "%"}</p>
    </div>
  );
});

const PredictResultsList: FC = () => {
  const { results } = usePrediction();
  if (!results) return null;
  if (results.length === 0) return null;
  return (
    <div className="no-scrollbar absolute bottom-20 z-20 flex w-10/12 gap-2 overflow-scroll">
      {results.map((result) => (
        <PredictResultItem key={result.id} result={result} />
      ))}
    </div>
  );
};

export default PredictResultsList;
