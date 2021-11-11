import store from '../store/configureStore';

export interface IUser {
  email: string,
  emailVerified: boolean,
  sub: string,
  token: string,
}
export interface IProject {
  name: string,
  description?: string,
  uuid: string,
  repositories?: IRepository[]
}

export interface IRepository {
  uuid: string,
  url: string,
  name: string,
  description?: string
}
// Infer the `RootState type from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch
