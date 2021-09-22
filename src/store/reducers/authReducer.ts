import { AnyAction } from 'redux';
import { ActionType } from '../actionTypes';
import { IUser } from '../../types/types';

interface IAuthState {
  user: IUser | null
}

const initState: IAuthState = {
  user: null,
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
      return { ...initState };
    }
    default: {
      return state;
    }
  }
}
