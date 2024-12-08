import { useCallback, useEffect, useState } from "react";
import { useWindowEvent } from "./useWindowEvent";

const eventListerOptions = {
  passive: true,
};

export const useViewportSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: 0,
    height: 0,
  });

  const setSize = useCallback(() => {
    setWindowSize({
      width: window.innerWidth || 0,
      height: window.innerHeight || 0,
    });
  }, []);

  useWindowEvent("resize", setSize, eventListerOptions);
  useWindowEvent("orientationchange", setSize, eventListerOptions);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(setSize, []);

  return windowSize;
};
