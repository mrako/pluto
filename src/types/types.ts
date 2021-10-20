import store from '../store/configureStore';

export interface IUser {
  email: string,
  emailVerified: boolean,
  sub: string,
}
export interface IProject {
  name: string,
  description?: string,
  uuid: string,
}

// Infer the `RootState type from the store itself
export type RootState = ReturnType<typeof store.getState>;
