import { applyMiddleware, createStore, Store } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension/developmentOnly';

import thunk from 'redux-thunk';

import reducer from './reducers/index';

import Api from './api/Api';

const api = new Api();

export default function configureStore(): Store {
  const composeEnhancers = composeWithDevTools({
    // options like actionSanitizer, stateSanitizer
  });
  const store = createStore(reducer, /* preloadedState, */ composeEnhancers(
    applyMiddleware(thunk.withExtraArgument(api)),
    // other store enhancers if any
  ));

  return store;
}
