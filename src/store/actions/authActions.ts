import { Dispatch } from 'redux';
import { Auth } from 'aws-amplify';
import { ActionType, Action } from '../actionTypes';

export const login = () => async (dispatch: Dispatch<Action>): Promise<void> => {
  const userDetails = await Auth.currentAuthenticatedUser();
  const user = {
    email: userDetails.attributes.email,
    emailVerified: userDetails.attributes.email_verified,
    sub: userDetails.attributes.sub,
  };
  localStorage.setItem('user', JSON.stringify(user));
  dispatch({
    type: ActionType.SIGNIN,
    payload: user,
  });
};

export const logout = () => (dispatch: Dispatch<Action>): void => {
  localStorage.removeItem('user');
  dispatch({
    type: ActionType.SIGNOUT,
  });
};
