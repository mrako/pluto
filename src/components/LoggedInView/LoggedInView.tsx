import { AmplifySignOut } from '@aws-amplify/ui-react';
import React, { ReactElement } from 'react';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import * as authActions from '../../store/actions/authActions';

import logo from './logo.svg';

export default function LoggedInView(): ReactElement {
  const history = useHistory();
  const dispatch = useDispatch();
  const handleSignOut = (authState: string) => {
    if (authState === 'signedout') {
      dispatch(authActions.logout());
      history.push('/login');
    }
  };
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <AmplifySignOut
          handleAuthStateChange={handleSignOut}
        />
      </header>
    </div>
  );
}
