import React, { ReactElement, useEffect } from 'react';
import Amplify, { Auth } from 'aws-amplify';
import { Provider } from 'react-redux';
import { AmplifyAuthenticator, AmplifySignOut, AmplifySignUp } from '@aws-amplify/ui-react';
import configureStore from './store/configureStore';
import config from './aws-exports';
import logo from './logo.svg';
import './App.css';

Amplify.configure(config);
const store = configureStore();

function App(): ReactElement {
  useEffect(() => {
    Auth.currentAuthenticatedUser().then((res) => console.log(res));
  });
  return (
    <Provider store={store}>
      <AmplifyAuthenticator>
        <AmplifySignUp
          slot="sign-up"
          formFields={[
            {
              type: 'username',
              label: 'Email',
              placeholder: 'Email',
              inputProps: { required: true, autocomplete: 'username' },
            },
            {
              type: 'password',
              label: 'Password',
              placeholder: 'Password',
              inputProps: { required: true, autocomplete: 'new-password' },
            },
          ]}
        />

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
            <AmplifySignOut />
          </header>
        </div>
      </AmplifyAuthenticator>
    </Provider>
  );
}
export default App;
