import { Auth } from 'aws-amplify';
import React, {
  ReactElement, useCallback, useEffect, useState,
} from 'react';
import { useDispatch } from 'react-redux';
import {
  Route, RouteProps, useHistory, useLocation,
} from 'react-router-dom';
import { logout } from 'store/actions/authActions';
import PageContent from 'stories/composite/PageContent/PageContent';
import TopNav from 'stories/composite/TopNav/TopNav';

export default function PrivateRoute({ children, ...rest }: RouteProps): ReactElement {
  const [auth, setAuth] = useState(false);
  const history = useHistory();
  const location = useLocation();
  const dispatch = useDispatch();

  const onHome = useCallback(() => {
    history.push('/home');
  }, [history]);
  const onLogout = useCallback(async () => {
    await Auth.signOut();
    dispatch(logout());
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
