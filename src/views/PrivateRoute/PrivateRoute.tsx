import { Auth } from 'aws-amplify';
import React, {
  ReactElement, useCallback, useEffect, useState,
} from 'react';
import { Route, RouteProps, useHistory } from 'react-router-dom';
import PageContent from 'stories/composite/PageContent/PageContent';
import TopNav from 'stories/composite/TopNav/TopNav';

export default function PrivateRoute({ children, ...rest }: RouteProps): ReactElement {
  const [auth, setAuth] = useState(false);
  const history = useHistory();

  const onHome = useCallback(() => {
    history.push('/home');
  }, [history]);
  const onLogout = useCallback(async () => {
    await Auth.signOut();
    setAuth(false);
    history.push('/login');
  }, [history]);

  useEffect(() => {
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
    isAuthenticated();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Route {...rest}>
      <TopNav onHome={onHome} onLogout={onLogout} />
      <PageContent>{ auth ? children : null }</PageContent>
    </Route>
  );
}
