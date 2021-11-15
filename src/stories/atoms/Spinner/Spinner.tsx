import React, { ReactElement } from 'react';
import styles from './Spinner.module.css';
import { Props } from './types';

const Spinner = ({ inverted, id }: Props): ReactElement => (
  <div id={id} className={`${styles.spinner}${inverted ? ` ${styles.inverted}` : ''}`}>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
);
export default Spinner;
