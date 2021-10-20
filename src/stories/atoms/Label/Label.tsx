import React, { ReactElement } from 'react';
import Info from '../Info/Info';
import styles from './Label.module.css';
import { LabelProps } from './types';

export default function Label({
  htmlFor, text, disabled, color = 'blue', info, className,
}: LabelProps): ReactElement {
  return (
    <div className={className}>
      <label
        htmlFor={htmlFor}
        className={`${styles.label} ${disabled ? styles['disabled-label'] : ''}`}
      ><span>{text}</span>
        {info ? <Info content={info} color={color} /> : null}
      </label>
    </div>
  );
}
