import { ReactNode } from 'react';
import { IconName, IconColor } from '../Icon/types';

export interface ButtonProps {
  /** Returns event object */
  onClick?: React.MouseEventHandler<HTMLButtonElement>,
  /** Button is disabled */
  disabled?: boolean,
  /** Button type */
  type?: ButtonType,
  /** Optional icon by name */
  icon?: IconName,
  /** Optional icons color */
  iconColor?: IconColor,
  /** Icon placement */
  iconPlace?: ButtonIconPlace,
  /** Icon's name for screen readers. If there is only icon in the button there must be a aria label for the icon. */
  /* TODO: check that either children or ariaIconLabel contain something */
  ariaIconLabel?: string,
  /** You may give extra CSS classes for the button */
  className?: string,
  loading?: boolean,
  /** This is the text to be rendered inside the button */
  children?: ReactNode,
  variant?: ButtonVariant
  /** Text that should be shown for screen readers while the button is in loading state  */
  ariaLoadingText?: string,
  /** Takes the whole available horizontal space */
  fluid?: boolean,
  id?: string,
}
type ButtonType = 'button' | 'submit';
type ButtonIconPlace = 'left' | 'right';
type ButtonVariant = 'primary' | 'secondary' | 'link';
