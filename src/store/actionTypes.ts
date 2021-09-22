import { IUser } from '../types/types';

export enum ActionType {
  SIGNIN = 'SIGNIN',
  SIGNOUT = 'SIGNOUT',
}

interface actionSignin {
  type: ActionType.SIGNIN;
  payload: IUser;
}

interface actionSignout {
  type: ActionType.SIGNOUT;
}

export type Action = actionSignin | actionSignout;
