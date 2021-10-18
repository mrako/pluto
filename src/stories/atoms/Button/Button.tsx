import React, { ReactElement } from 'react';
import styles from './Button.module.css';

import Icon from '../Icon/Icon';
import { ButtonProps } from './types';

const assignButtonClass = (variant: ButtonProps['variant']) => {
  let className = `${styles.btn}`;
  switch (variant) {
    case 'primary':
      className += ` ${styles['btn-primary']}`;
      break;
    case 'secondary':
      className += ` ${styles['btn-secondary']}`;
      break;
    case 'link':
      className += ` ${styles['btn-link']}`;
      break;
    default:
  }
  return className;
};

const defaultIconColor = (variant: ButtonProps['variant']) => {
  switch (variant) {
    case 'primary':
      return 'white';
    case 'secondary':
    case 'link':
      return 'primary';
    default:
  }
  return 'primary';
};

export default function Button({
  onClick, icon, iconColor, iconPlace = 'left', ariaIconLabel, variant = 'primary', children, className, disabled,
  loading, type = 'button', ariaLoadingText, fluid = false, id, ...rest
}: ButtonProps): ReactElement {
  let classForButton = assignButtonClass(variant);
  if (className) {
    classForButton += ` ${className}`;
  }
  if (loading) {
    classForButton += ` ${styles['btn-loading']}`;
  }
  if (disabled) {
    classForButton += ` ${styles.disabled}`;
  }
  if (fluid) {
    classForButton += ` ${styles.fluid}`;
  }

  return (
    <button
      type={type}
      disabled={disabled}
      className={classForButton}
      onClick={onClick}
      id={id}
      {...rest}
    >
      {loading
        ? (
          <>
            <span className={styles['loading-animation']} />
            <span className="sr-only">{ariaLoadingText}</span>
          </>
        )
        : null}
      {/* Have to have two versions for icons so that if there is no text content in the button that there is no margins */}
      {children
        ? (
          <>
            {/* button with icon + children */}
            <span className={`${styles['btn-text']}`}>
              {icon && iconPlace === 'left' ? (
                <>
                  <Icon width={16} height={16} color={iconColor || defaultIconColor(variant)} name={icon} aria-label={ariaIconLabel} className={styles['btn-icon-left']} />
                </>
              ) : null}
              {children}
              {icon && iconPlace === 'right' ? (
                <>
                  <Icon width={16} height={16} color={iconColor || defaultIconColor(variant)} name={icon} aria-label={ariaIconLabel} className={styles['btn-icon-right']} />
                </>
              ) : null}
            </span>
          </>
        ) : (
          <>
            {icon ? <Icon width={16} height={16} color={iconColor || defaultIconColor(variant)} name={icon} aria-label={ariaIconLabel} className={styles['btn-icon-only']} /> : null}
          </>
        )}
    </button>
  );
}
