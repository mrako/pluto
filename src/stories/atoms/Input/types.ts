import React from 'react';
import { IconName } from '../Icon/types';

export interface InputProps {
  /** Use this to make this component a controlled component */
  value?: string,
  /** Name of input */
  name?: string,
  /** Gives the default value for the input */
  defaultValue?: string,
  placeholder?: string,
  /** Type of input */
  type?: 'text' | 'number' | 'email' | 'password',
  /** Id of input */
  id?: string,
  /** Default input onChange. Can be debounced with prop debounceTimer */
  onChange?: React.ChangeEventHandler<HTMLInputElement>;
  /** Icon for input */
  icon?: IconName,
  className?: string,
  disabled?: boolean,
  /** color variant */
  variant?: 'primary' | 'secondary',
  fluid?: boolean,
  /** Error can have a message (string) or can be only a red outline (boolean) */
  error?: boolean | string,
  /** This prop sets debouncing for the input. A good value is 300 */
  debounceTimer?: number,
  /** Adds label to input */
  label?: string,
  /** Adds Info to label. Requires label prop */
  info?: string,
}
