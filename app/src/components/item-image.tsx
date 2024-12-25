import { items } from "@/constants/items";
import { getItemStyles } from "@/utils/item";
import { FC } from "react";

interface Props {
  itemId: string | null | undefined;
}

const ItemImage: FC<Props> = (props) => {
  const { itemId } = props;
  if (!itemId) return null;
  const item = items[itemId];
  return (
    <img
      className="mt-2"
      src="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
      style={getItemStyles(item)}
      alt={item.name + " " + item.description}
    />
  );
};

export default ItemImage;
