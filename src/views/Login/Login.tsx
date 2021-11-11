import { AmplifyAuthenticator, AmplifySignUp } from '@aws-amplify/ui-react';
import React, { ReactElement } from 'react';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import * as authActions from 'store/actions/authActions';
import './Login.css';

interface IHistoryFrom {
  from: {
    hash: string,
    key: string,
    pathname: string,
    search: string,
  }
}
export default function Login(): ReactElement {
  const history = useHistory();
  const dispatch = useDispatch();
  const handleAuthStateChange = async (authState: string) => {
    if (authState === 'signedin') {
      await dispatch(authActions.login());
      if (history.location.state) {
        const historyState = history.location.state as IHistoryFrom;
        history.push(historyState.from.pathname + historyState.from.search);
      } else if (history.location.pathname === '/login') {
        history.push('/home');
      }
    }
  };
  return (
    <AmplifyAuthenticator
      handleAuthStateChange={handleAuthStateChange}
    >
      <AmplifySignUp
        slot="sign-up"
        formFields={[
          {
            type: 'email',
            label: 'Email',
            placeholder: 'Email',
            inputProps: { required: true, autocomplete: 'email' },
          },
          {
            type: 'username',
            label: 'Username',
            placeholder: 'Username',
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
    </AmplifyAuthenticator>
  );
}
