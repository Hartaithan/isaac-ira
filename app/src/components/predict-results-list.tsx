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
  const { size = 50, item } = props;
  return (
    <div className="overflow-hidden" style={{ width: size, height: size }}>
      <div
        className="relative scale-50"
        style={{ width: size * 2, height: size * 2 }}
      >
        <img
          className="absolute -translate-x-1/2 -translate-y-1/2 transform"
          src="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
          style={getItemStyles(item)}
          alt={item.name + " " + item.description}
        />
      </div>
    </div>
  );
};

const PredictResultItem: FC<ItemProps> = memo((props) => {
  const { result } = props;
  const item = items[result.id];
  return (
    <div className="flex min-w-24 flex-col items-center rounded bg-neutral-900/80 px-3 py-2 text-center text-white">
      <ItemImage item={item} />
      <p className="font-bold">{item?.name || "Not found"}</p>
      <p>{result.probability + "%"}</p>
    </div>
  );
});

const PredictResultsList: FC = () => {
  const { results } = usePrediction();
  if (!results) return null;
  if (results.length === 0) return null;
  return (
    <div className="no-scrollbar absolute bottom-20 z-20 flex w-10/12 justify-center gap-2 overflow-scroll">
      {results.map((result) => (
        <PredictResultItem key={result.id} result={result} />
      ))}
    </div>
  );
};

export default PredictResultsList;
