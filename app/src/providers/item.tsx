import ItemModal from "@/components/item-modal";
import { useModal } from "@/hooks/use-modal";
import {
  createContext,
  FC,
  PropsWithChildren,
  useContext,
  useMemo,
} from "react";

interface Context {
  item?: string | null;
  openModal: (
    data?: string | React.MouseEvent<HTMLButtonElement, MouseEvent> | null,
  ) => void;
}

const initialValue: Context = {
  item: null,
  openModal: () => null,
};

const Context = createContext<Context>(initialValue);

const ItemProvider: FC<PropsWithChildren> = (props) => {
  const { children } = props;
  const [modal, openModal, closeModal] = useModal<string | null>();

  const exposed: Context = useMemo(
    () => ({ item: modal.data, openModal }),
    [modal.data, openModal],
  );

  return (
    <Context.Provider value={exposed}>
      {children}
      <ItemModal
        data={modal.data}
        isVisible={modal.isVisible}
        onClose={closeModal}
      />
    </Context.Provider>
  );
};

export const useItem = (): Context => useContext(Context);

export default ItemProvider;
