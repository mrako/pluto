import React, { ReactElement } from 'react';
import Button from 'stories/atoms/Button/Button';
import styles from './TopNav.module.css';
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
        <h1 id="home" className={styles.home} onClick={onHome}>Pluto</h1>
        <Button id="logout" variant="link" icon="logout" iconPlace="right" className={styles.logout} onClick={onLogout}>Logout</Button>
      </nav>
      <div className={styles.below} />
    </>
  );
}
