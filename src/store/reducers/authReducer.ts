import { AnyAction } from 'redux';
import { ActionType } from '../actionTypes';
import { IUser } from '../../types/types';

interface IAuthState {
  user: IUser | null
}

const localStorageUser = localStorage.getItem('user');
const initState: IAuthState = {
  user: localStorageUser ? JSON.parse(localStorageUser) : null,
};

export default function auth(state:IAuthState = initState, action:AnyAction):IAuthState {
  switch (action.type) {
    case ActionType.SIGNIN: {
      return {
        ...state,
        user: action.payload,
      };
    }
    case ActionType.SIGNOUT: {
      return { ...initState, user: null };
    }
    default: {
      return state;
    }
  }
}
