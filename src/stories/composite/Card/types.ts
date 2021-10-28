import { IconName } from 'stories/atoms/Icon/types';

export interface CardProps {
  title: string,
  subtitle?: string,
  action?: React.MouseEventHandler<HTMLButtonElement>,
  actionTitle?: string,
  titleIcon?: IconName,
  id?: string,
}
