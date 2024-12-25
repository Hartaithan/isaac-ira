import { items } from "@/constants/items";
import type { FC } from "react";
import type { ModalProps } from "../ui/modal";
import { Modal } from "../ui/modal";
import ItemImage from "./item-image";

const ItemModal: FC<ModalProps<string | null>> = (props) => {
  const { isVisible, data, onClose } = props;
  if (!data) return null;
  const item = items[data];
  return (
    <Modal
      title={item.name}
      description="Date details modal"
      isVisible={isVisible}
      onClose={onClose}
    >
      <div className="flex flex-col items-center">
        <ItemImage itemId={data} />
        <p className="mt-2 font-semibold">{item.description}</p>
        <pre className="whitespace-pre-wrap">
          {JSON.stringify(item, null, 2)}
        </pre>
      </div>
    </Modal>
  );
};

export default ItemModal;
