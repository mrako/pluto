import React, { ReactElement } from 'react';
import Label from '../Label/Label';
import styles from './TextArea.module.css';
import { TextAreaProps } from './types';

export default function TextArea({
  name, onChange, value, placeholder, id, rows = 5, className, disabled, defaultValue, fluid, error, label, info,
}: TextAreaProps): ReactElement {
  // textarea
  let classForTextarea = className || '';
  if (disabled) {
    classForTextarea += ` ${styles['disabled-textarea']}`;
  }
  // wrapper
  let textareaWrapper = styles['textarea-wrapper'];
  if (fluid) {
    textareaWrapper += ` ${styles.fluid}`;
  }
  if (error) {
    textareaWrapper += ` ${styles['error-wrapper']}`;
    classForTextarea += ` ${styles['error-outline']}`;
  }

  return (
    <div className={textareaWrapper}>
      {label ? <Label htmlFor={id} className={styles.label} text={label} info={info} /> : null}
      <textarea
        name={name}
        disabled={disabled}
        defaultValue={defaultValue}
        onChange={onChange}
        value={value}
        placeholder={placeholder}
        id={id}
        rows={rows}
        className={classForTextarea}
      />
      {typeof (error) === 'string' ? <span className={`${styles.error}`}>{error}</span> : null}
    </div>
  );
}
