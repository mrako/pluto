import React, { ReactElement } from 'react';
import Amplify, { API } from 'aws-amplify';
import awsconfig from './aws-exports';
import logo from './logo.svg';
import './App.css';

Amplify.configure(awsconfig);
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
      console.log(response);
    })
    .catch((error) => {
      console.log(error.response);
    });
}

function App(): ReactElement {
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
        <br />
        <div>
          Reply from the projects endpoint: { getProjects() }
        </div>
      </header>
    </div>
  );
}

export default App;
