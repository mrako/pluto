import React, { ReactElement } from 'react';
import Amplify from 'aws-amplify';
import { Provider } from 'react-redux';
import {
  Router, Redirect, Route, Switch,
} from 'react-router-dom';
import history from 'customHistory';
import Install from './views/Install/Install';
import PrivateRoute from './views/PrivateRoute/PrivateRoute';
import store from './store/configureStore';
import config from './aws-exports';
import Login from './views/Login/Login';
import Home from './views/Home/Home';
import CreateProject from './views/CreateProject/CreateProject';
import Project from './views/Project/Project';

const amplifyConfig = {
  Auth: {
    mandatorySignIn: true,
    region: config.aws_project_region,
    userPoolId: config.aws_user_pools_id,
    identityPoolId: config.aws_cognito_identity_pool_id,
    userPoolWebClientId: config.aws_user_pools_web_client_id,
  },
  API: {
    endpoints: [
      {
        name: 'api',
        region: process.env.REACT_APP_REGION,
        endpoint: process.env.REACT_APP_PROJECT_API_URL,
      },
    ],
  },
};

Amplify.configure(amplifyConfig);

function App(): ReactElement {
  return (
    <Provider store={store}>
      <Router history={history}>
        <Switch>
          <PrivateRoute exact path="/home">
            <Home />
          </PrivateRoute>
          <PrivateRoute exact path="/project/create">
            <CreateProject />
          </PrivateRoute>
          <PrivateRoute exact path="/project/:uuid">
            <Project />
          </PrivateRoute>
          <PrivateRoute exact path="/install">
            <Install />
          </PrivateRoute>
          <Route exact path="/login">
            <Login />
          </Route>
          <Route>
            <Redirect to="/home" />
          </Route>
        </Switch>
      </Router>
    </Provider>
  );
}
export default App;
