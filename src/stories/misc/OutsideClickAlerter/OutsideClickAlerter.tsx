import React, {
  useEffect, useRef, ReactElement,
} from 'react';

interface ClickOutsideProps {
  /** Fires this when clicked outside of it's children */
  onOutsideClick(e: MouseEvent): void;
  /** Children that do not fire onOutsideClick */
  children: React.ReactElement;
}
export default function OutsideClickAlerter({ children, onOutsideClick }: ClickOutsideProps): ReactElement {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!ref?.current) {
      return undefined;
    }
    const handleClickOutside = (e: MouseEvent) => {
      if (onOutsideClick && !ref?.current?.contains(e.target as Node)) {
        onOutsideClick(e);
      }
    };
    document.addEventListener('click', handleClickOutside);
    return function cleanup() {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [onOutsideClick, ref]);
  return (<span ref={ref}>{children}</span>);
}
