import React, { ReactElement } from 'react';
import Amplify from 'aws-amplify';
import { Provider } from 'react-redux';
import {
  BrowserRouter, Route, Switch,
} from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute/PrivateRoute';
import store from './store/configureStore';
import config from './aws-exports';
import './App.css';
import Login from './components/Login/Login';
import LoggedInView from './components/LoggedInView/LoggedInView';

Amplify.configure(config);

function App(): ReactElement {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Switch>
          <PrivateRoute exact path="/">
            <LoggedInView />
          </PrivateRoute>
          <Route path="/login/">
            <Login />
          </Route>
        </Switch>
      </BrowserRouter>
    </Provider>
  );
}
export default App;
