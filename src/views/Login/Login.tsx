import { AmplifyAuthenticator, AmplifySignUp } from '@aws-amplify/ui-react';
import React, { ReactElement } from 'react';
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import * as authActions from 'store/actions/authActions';
import './Login.css';

export default function Login(): ReactElement {
  const history = useHistory();
  const dispatch = useDispatch();
  const handleAuthStateChange = (authState: string) => {
    if (authState === 'signedin') {
      dispatch(authActions.login());
      history.push('/home');
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
    </AmplifyAuthenticator>
  );
}
