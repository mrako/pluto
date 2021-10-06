import { IconColor } from '../Icon/types';

export interface LabelProps {
  /** should match your input id */
  htmlFor?: string,
  text: string,
  /** if the input is disabled, so should be the label */
  disabled?: boolean,
  /** render an Info component with this content */
  info?: string,
  /** Color of the info Icon */
  color?: IconColor,
}
