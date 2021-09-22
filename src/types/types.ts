import store from '../store/configureStore';

export interface IUser {
  email: string,
  emailVerified: boolean,
  sub: string,
}

// Infer the `RootState type from the store itself
export type RootState = ReturnType<typeof store.getState>
