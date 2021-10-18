import { CSSProperties, MouseEventHandler } from 'react';

export interface IconProps {
  /** Name of icon */
  name?: IconName,
  /** Width of the icon in pixels. Will overwrite the width from size */
  width?: number,
  /** Height of the icon in pixels. Will overwrite the height from size */
  height?: number,
  /** Id of the icon */
  id?: string,
  /** Extra css classes */
  className?: string,
  /** Aria label attribute for the icon */
  ariaLabel?: string,
  /** Additional inline styles */
  style?: CSSProperties | undefined,
  /** Size of the icon */
  size?: IconSize
  /** an Onclick event handler */
  onClick?: MouseEventHandler<SVGSVGElement>
  /** Makes cursor a pointer */
  actionable?: boolean,
  /** Color of the Icon */
  color?: IconColor,
}

export type IconColor = 'primary' | 'secondary' | 'black' | 'white' | 'blue';
export type IconSize = 'mini' | 'tiny' | 'small' | 'medium' | 'large' | 'huge' | 'massive';
export type IconName = '' | 'fullArrowDown' | 'fullArrowRight' | 'arrowLeft' |
  'arrowRight' | 'arrowUp' | 'arrowDown' | 'edit' |
  'close' | 'cancel' | 'delete' | 'add' | 'backgroundPlus' | 'details' |
  'link' | 'logout' | 'checkmark' | 'filledCheckmark' | 'hollowCheckmark' | 'warning' | 'info' | 'search' | undefined;
