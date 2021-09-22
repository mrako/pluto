import { Auth } from 'aws-amplify';
import React, {
  ReactElement, useEffect, useState,
} from 'react';
import { Route, RouteProps, useHistory } from 'react-router-dom';

export default function PrivateRoute({ children, ...rest }: RouteProps): ReactElement {
  const [auth, setAuth] = useState(false);
  const history = useHistory();

  const isAuthenticated = () => {
    setAuth(false);

    const redirectToLogin = () => {
      history.push('/login');
    };
    Auth.currentSession().then((response) => {
      if (response.isValid()) {
        setAuth(true);
      } else {
        redirectToLogin();
      }
    }).catch(() => {
      redirectToLogin();
    });
  };

  useEffect(() => {
    isAuthenticated();
  }, []);

  return (
    <Route {...rest}>
      { auth ? children : null }
    </Route>
  );
}
