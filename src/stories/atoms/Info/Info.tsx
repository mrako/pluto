import React, { ReactElement } from 'react';
import Popup from '../Popup/Popup';
import Icon from '../Icon/Icon';
import { InfoProps } from './types';

export default function Info({
  content, icon = 'info', color = 'blue', size = 'tiny', id, className,
}: InfoProps):ReactElement {
  return (
    <Popup
      trigger={(
        <Icon className={className} id={id} color={color} name={icon} size={size} />
      )}
      position="center"
      on="hover"
      content={content}
    />
  );
}
