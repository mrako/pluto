import { IconName, IconColor, IconSize } from '../Icon/types';

export interface InfoProps {
  id?: string,
  /** Additional css classes for the trigger */
  className?: string,
  /** Content of the info */
  content: string,
  /** Check Icon component for names */
  icon?: IconName,
  /** Check Icon component for colors */
  color?: IconColor,
  /** Check Icon component for sizes */
  size?: IconSize,
}
