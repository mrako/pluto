import React, { ReactElement } from 'react';
import styles from './TopNav.module.css';
import Button from '../Button/Button';
// import { ButtonProps } from './types';

interface TopNavProps {
  onLogout: () => void,
  onHome: () => void,
}

export default function TopNav({
  onLogout, onHome,
}: TopNavProps): ReactElement {
  return (
    <>
      <nav className={styles['top-nav']}>
        <div className={styles.home} onClick={onHome}>Pluto</div>
        <Button variant="link" className={styles.logout} onClick={onLogout}>Logout</Button>
      </nav>
      <div className={styles.below} />
    </>
  );
}
