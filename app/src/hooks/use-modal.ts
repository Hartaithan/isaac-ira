import type { MouseEvent } from "react";
import { useCallback, useState } from "react";
import type { ModalState } from "../ui/modal";

export const useModal = <T = null>() => {
  const [state, setState] = useState<ModalState<T>>({
    isVisible: false,
    data: null as T,
  });

  const handleOpen = useCallback((data?: T | MouseEvent<HTMLButtonElement>) => {
    if (data && data instanceof Object && "preventDefault" in data) {
      setState((prev) => ({ ...prev, isVisible: true }));
    } else {
      setState((prev) => ({ ...prev, isVisible: true, data }));
    }
  }, []);

  const handleClose = useCallback((value: boolean) => {
    if (value) setState((prev) => ({ ...prev, isVisible: value }));
    else setState((prev) => ({ ...prev, isVisible: false }));
  }, []);

  return [state, handleOpen, handleClose] as const;
};
