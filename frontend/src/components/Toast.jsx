import { useEffect, useRef, useCallback } from "react";

export default function Toast({ message, type = "info", onClose }) {
  const timerRef = useRef(null);

  const dismiss = useCallback(() => {
    if (onClose) onClose();
  }, [onClose]);

  useEffect(() => {
    if (message) {
      timerRef.current = setTimeout(dismiss, 3500);
    }
    return () => clearTimeout(timerRef.current);
  }, [message, dismiss]);

  if (!message) return null;

  return (
    <div className={`toast toast-${type} visible`}>
      {message}
    </div>
  );
}
