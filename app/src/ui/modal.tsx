import { XIcon } from "lucide-react";
import type { ButtonProps } from "../ui/button";
import { Button } from "../ui/button";
import {
  Dialog,
  DialogCloseStyles,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";

import { cn } from "@/utils/styles";
import { FC, PropsWithChildren } from "react";

export interface ModalState<T = null> {
  data?: T;
  isVisible: boolean;
}

export interface ModalProps<T = null> extends PropsWithChildren, ModalState<T> {
  onClose: (value: boolean) => void;
  title?: string;
  description?: string;
}

const Modal: FC<ModalProps> = (props) => {
  const { isVisible, title, description, children, onClose } = props;
  return (
    <Dialog open={isVisible} onOpenChange={onClose}>
      <DialogContent className="w-[calc(100%-1.5rem)] rounded-lg px-4 py-3 md:w-full">
        <DialogHeader className="space-y-3">
          {title && (
            <DialogTitle className="w-full text-center text-sm font-medium md:text-base">
              {title}
            </DialogTitle>
          )}
          <DialogDescription className="hidden">
            {description ?? "Modal"}
          </DialogDescription>
        </DialogHeader>
        {children}
      </DialogContent>
    </Dialog>
  );
};
Modal.displayName = "Modal";

export const ModalCloseButton: FC<ButtonProps> = (props) => {
  const { className, ...rest } = props;
  return (
    <Button
      unstyled
      aria-label="Close modal"
      className={cn(DialogCloseStyles.button, className)}
      {...rest}
    >
      <XIcon className={DialogCloseStyles.icon} />
      <span className={DialogCloseStyles.sr}>Close</span>
    </Button>
  );
};
ModalCloseButton.displayName = "ModalCloseButton";

export { Modal };
