import { useEffect } from "react";

export const useWindowEvent = <K extends string>(
  type: K,
  listener: K extends keyof WindowEventMap
    ? (this: Window, ev: WindowEventMap[K]) => void
    : (this: Window, ev: CustomEvent) => void,
  options?: boolean | AddEventListenerOptions,
) => {
  useEffect(() => {
    window.addEventListener(type as never, listener, options);
    return () => window.removeEventListener(type as never, listener, options);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [type, listener]);
};
