import { IAction } from '../types/actions';

interface IAuthState {
  key?: string
}

const initState: IAuthState = {
};

export default function auth(state = initState, action:IAction): IAuthState {
  switch (action.type) {
    default: {
      return state;
    }
  }
}
