import React from 'react';

export interface TextAreaProps {
  name?: string,
  placeholder?: string,
  /** Defines the size */
  rows?: number,
  value?: string,
  /** Gives the default value for the textarea */
  defaultValue?: string,
  id?: string,
  /** Returns event object */
  onChange?: React.ChangeEventHandler<HTMLTextAreaElement>,
  disabled?: boolean,
  className?: string,
  fluid?: boolean,
  /** Error can have a message or can be only a red outline */
  error?: string | boolean,
  /** Adds label to input */
  label?: string,
  /** Adds Info to label. Requires label prop */
  info?: string,
}
