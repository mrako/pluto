import { AmplifySignOut } from '@aws-amplify/ui-react';
import React, { ReactElement, useState } from 'react';
import { API } from 'aws-amplify';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import * as authActions from '../../store/actions/authActions';

import logo from './logo.svg';

export default function LoggedInView(): ReactElement {
  const [projects, setProjects] = useState('');
  const history = useHistory();
  const dispatch = useDispatch();
  const handleSignOut = (authState: string) => {
    if (authState === 'signedout') {
      dispatch(authActions.logout());
      history.push('/login');
    }
  };
  const apiName = 'projects';
  const path = '/projects';
  const myInit = {
    headers: {},
    response: true,
    queryStringParameters: {
      name: 'param',
    },
  };

  function getProjects() {
    API
      .get(apiName, path, myInit)
      .then((response) => {
        setProjects(response.data);
      });
  }
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
        <button onClick={getProjects}>Test API here</button>
        {projects}
        <AmplifySignOut
          handleAuthStateChange={handleSignOut}
        />
      </header>
    </div>
  );
}
