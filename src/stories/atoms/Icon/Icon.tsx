import React, {
  FunctionComponent, ReactElement, SVGProps,
} from 'react';
import styles from './Icon.module.css';
import * as icons from './icons';
import { IconProps } from './types';

const iconSize = (size: IconProps['size']) => {
  switch (size) {
    case 'massive':
      return 36;
    case 'huge':
      return 33;
    case 'large':
      return 30;
    case 'medium':
      return 28;
    case 'small':
      return 16;
    case 'tiny':
      return 12;
    case 'mini':
      return 10;
    default:
      return '';
  }
};

export default function Icon({
  name = '', width, height, id = '', className = '', ariaLabel = '', style, size = 'medium', onClick, actionable = false, color = 'black',
}: IconProps): ReactElement | null {
  let ImportedIcon: FunctionComponent<SVGProps<SVGSVGElement>> | null = null;
  if (name) {
    ImportedIcon = icons[name];
  }
  const currentIconSize = iconSize(size);
  const classForIcon = `${className || ''} ${actionable ? styles.actionable : ''}`;
  if (ImportedIcon) {
    return (
      <ImportedIcon
        id={id}
        className={`${styles.icon} ${classForIcon} ${styles[`${color}`]}`}
        width={width || currentIconSize}
        height={height || currentIconSize}
        aria-label={ariaLabel}
        style={style}
        onClick={onClick}
      />
    );
  }
  return null;
}
