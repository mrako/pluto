import auth from './authReducer';
import { ActionType, Action } from '../actionTypes';

describe('authReducer', () => {
  it('sets the state correctly on SIGNIN event', () => {
    const state = { user: null };
    const newUser = { sub: 'example', email: 'example@example.com', emailVerified: true };
    const action: Action = { type: ActionType.SIGNIN, payload: newUser };
    const newState = auth(state, action);

    expect(newState).toEqual({ user: newUser });
  });

  it('sets the state correctly on SIGNOUT event', () => {
    const state = { user: { sub: 'example', email: 'example@example.com', emailVerified: true } };
    const action: Action = { type: ActionType.SIGNOUT };
    const newState = auth(state, action);
    expect(newState).toEqual({ user: null });
  });
});
