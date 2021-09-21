import { configureStore } from '@reduxjs/toolkit';
import auth from './reducers/authReducer';

const store = configureStore({
  reducer: {
    auth,
  },
});

export default store;

export type RootState = ReturnType<typeof store.getState>
