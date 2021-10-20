import { Auth } from 'aws-amplify';
import React, {
  ReactElement, useCallback, useEffect, useState,
} from 'react';
import {
  Route, RouteProps, useHistory, useLocation,
} from 'react-router-dom';
import PageContent from 'stories/composite/PageContent/PageContent';
import TopNav from 'stories/composite/TopNav/TopNav';

export default function PrivateRoute({ children, ...rest }: RouteProps): ReactElement {
  const [auth, setAuth] = useState(false);
  const history = useHistory();
  const location = useLocation();

  const onHome = useCallback(() => {
    history.push('/home');
  }, [history]);
  const onLogout = useCallback(async () => {
    await Auth.signOut();
    setAuth(false);
    history.push('/login');
  }, [history]);

  useEffect(() => {
    const redirectToLogin = () => {
      history.push('/login', { from: location });
    };
    Auth.currentSession().then((response) => {
      if (response.isValid()) {
        setAuth(true);
      } else {
        setAuth(false);
        redirectToLogin();
      }
    }).catch(() => {
      setAuth(false);
      redirectToLogin();
    });
  }, [history, location]);

  return (
    <Route {...rest}>
      {auth ? (
        <>
          <TopNav onHome={onHome} onLogout={onLogout} />
          <PageContent>{children}</PageContent>
        </>
      ) : null}

    </Route>
  );
}
