import React from 'react';
import _ from 'lodash';
import Icon from '../Icon/Icon';
import styles from './Input.module.css';
import { InputProps } from './types';
import Label from '../Label/Label';

export default function Input({
  value, name, defaultValue, placeholder, type = 'text', id, onChange = () => { /* */ }, icon,
  className, disabled, variant = 'primary', fluid, error, debounceTimer, label, info,
}: InputProps): React.ReactElement {
  let debouncedOnChange: _.DebouncedFunc<(event: React.ChangeEvent<HTMLInputElement>) => void>;
  if (debounceTimer) {
    debouncedOnChange = _.debounce((event) => {
      onChange(event);
    }, debounceTimer);
  }
  let classForInput = className || '';
  if (disabled) {
    classForInput += ` ${styles['disabled-input']}`;
  }
  if (icon) {
    classForInput += ` ${styles['custom-indent']}`;
  }
  // wrapper
  let inputWrapper = styles['text-input-wrapper'];
  if (fluid) {
    inputWrapper += ` ${styles.fluid}`;
  }
  if (error) {
    inputWrapper += ` ${styles['error-wrapper']}`;
    classForInput += ` ${styles['error-outline']}`;
  }
  if (variant) {
    inputWrapper += ` ${styles[variant]}`;
  }
  return (
    <div className={inputWrapper}>
      {label ? <Label htmlFor={id} className={styles.label} text={label} info={info} /> : null}
      <input
        name={name}
        defaultValue={defaultValue}
        onChange={
          (e) => {
            if (debounceTimer) {
              e.persist();
              debouncedOnChange(e);
            } else {
              onChange(e);
            }
          }
        }
        value={value}
        placeholder={placeholder}
        type={type}
        id={id}
        disabled={disabled}
        className={classForInput}
      />
      {icon
        ? (
          <Icon
            name={`${icon}`}
            className={`${styles['input-icon']} ${variant === 'primary' ? styles['input-icon-primary'] : styles['input-icon-secondary']} ${disabled ? styles['disabled-icon'] : ''}`}
          />
        ) : null}
      {typeof (error) === 'string' ? <span className={`${styles.error}`}>{error}</span> : null}
    </div>
  );
}
