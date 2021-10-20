import React, { ReactElement } from 'react';
import Button from 'stories/atoms/Button/Button';
import Icon from 'stories/atoms/Icon/Icon';

import styles from './Card.module.css';
import { CardProps } from './types';

export default function Card({
  title, subtitle, action, actionTitle, titleIcon, id,
}: CardProps):ReactElement {
  return (
    <div className={styles.container} id={id}>
      <h2 className={styles.title}>
        {titleIcon ? <Icon className={styles['title-icon']} width={13} height={17} name={titleIcon} /> : null }
        {title}
      </h2>
      {subtitle ? <div className={styles.subtitle}>{subtitle}</div> : null}
      {action ? <Button id={`${id}-button`} onClick={action}>{actionTitle}</Button> : null}
    </div>
  );
}
