import { configureStore } from '@reduxjs/toolkit';
import auth from './reducers/authReducer';
import project from './reducers/projectReducer';

const store = configureStore({
  reducer: {
    auth,
    project,
  },
});

export default store;

export type RootState = ReturnType<typeof store.getState>
