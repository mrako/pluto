/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
import React, {
  useEffect, useState, ReactElement,
} from 'react';
import _ from 'lodash';
import OutsideClickAlerter from 'stories/misc/OutsideClickAlerter/OutsideClickAlerter';
import Portal from 'stories/misc/Portal/Portal';
import styles from './Popup.module.css';
import { PopupProps } from './types';

interface ICords {
  left?: number,
  top?: number,
}

export default function Popup({
  position = 'top', xOffset = 0, yOffset = 0, on = 'hover', trigger, content, children, contentClasses, className, id, borderless,
}: PopupProps):ReactElement {
  const [show, setShow] = useState(false);
  const [cords, setCords] = useState<ICords>({});

  const triggerRef = React.useRef<HTMLDivElement>(null);
  const popupRef = React.useRef<HTMLSpanElement>(null);
  function getCords(override = false) {
    if (!override && !show) {
      return;
    }
    const triggerRect = triggerRef?.current?.getBoundingClientRect();
    const popupRect = popupRef?.current?.getBoundingClientRect();
    if (!triggerRect || !popupRect) {
      return;
    }
    if (position === 'center') {
      setCords({
        left: triggerRect.left - 19 + triggerRect.width / 2 + xOffset,
        top: triggerRect.top + window.scrollY - popupRect.height - 8 + yOffset,
      });
    } else if (position === 'center-bottom') {
      setCords({
        left: triggerRect.left - 19 + triggerRect.width / 2 + xOffset,
        top: triggerRect.top + window.scrollY + triggerRect.height + 8 + yOffset,
      });
    } else if (position === 'top') {
      setCords({
        left: triggerRect.left + xOffset,
        top: triggerRect.top + window.scrollY - popupRect.height - 8 + yOffset,
      });
    } else if (position === 'bottom') {
      setCords({
        left: triggerRect.left + xOffset,
        top: triggerRect.top + window.scrollY + triggerRect.height + 8 + yOffset,
      });
    } else if (position === 'top-right') {
      setCords({
        left: triggerRect.right - popupRect.width + xOffset,
        top: triggerRect.top + window.scrollY - popupRect.height - 8 + yOffset,
      });
    } else if (position === 'bottom-right') {
      setCords({
        left: triggerRect.right - popupRect.width + xOffset,
        top: triggerRect.top + window.scrollY + triggerRect.height + 8 + yOffset,
      });
    }
  }
  useEffect(() => {
    if (show) {
      getCords();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [show]);
  function showPopupHandler() {
    setShow(true);
    getCords(true);
  }

  function close() {
    setShow(false);
  }

  function popupPosition() {
    const positionClass = `${styles.popup}`;
    if (position === 'bottom' || position === 'center-bottom') {
      return `${positionClass} ${styles.bottom}`;
    }
    if (position === 'top' || position === 'center') {
      return `${positionClass} ${styles.top}`;
    }
    if (position === 'top-right') {
      return `${positionClass} ${styles['top-right']}`;
    }
    return `${positionClass} ${styles['bottom-right']}`;
  }
  function onResize() {
    _.throttle(getCords, 100)();
  }
  useEffect(() => {
    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
    };
  });

  return (
    <>
      {on === 'hover' ? <div className={styles['trigger-wrapper']} ref={triggerRef} onMouseEnter={showPopupHandler} onMouseLeave={close}>{trigger}</div> : null }
      {on === 'click' ? <div className={styles['trigger-wrapper']} ref={triggerRef} onClick={show ? close : showPopupHandler}>{trigger}</div> : null }
      {content && !children && show ? (
        <Portal>
          <span
            className={`${popupPosition()}${borderless ? ` ${styles.borderless}` : ''}${className ? ` ${className}` : ''}`}
            style={{ ...cords }}
            id={id}
            ref={popupRef}
          >
            <OutsideClickAlerter onOutsideClick={on === 'click' ? close : () => { /* empty */ }}>
              <span
                className={
                  `${contentClasses ? `${styles['popup-content']} ${contentClasses}` : styles['popup-content']}`
                }
              >
                {content}
              </span>
            </OutsideClickAlerter>
          </span>
        </Portal>

      ) : null }
      {children && show ? (
        <Portal>
          <span
            className={`${popupPosition()}${borderless ? ` ${styles.borderless}` : ''}${className ? ` ${className}` : ''}`}
            style={{ ...cords }}
            id={id}
            ref={popupRef}
          >
            <OutsideClickAlerter onOutsideClick={on === 'click' ? close : () => { /* empty */ }}>
              {children}
            </OutsideClickAlerter>
          </span>
        </Portal>
      ) : null}
    </>
  );
}
