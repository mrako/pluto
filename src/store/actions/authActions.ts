import { Dispatch } from 'redux';
import { Auth } from 'aws-amplify';
import { ActionType, Action } from '../actionTypes';

export const login = () => async (dispatch: Dispatch<Action>): Promise<void> => {
  const userDetails = await Auth.currentAuthenticatedUser();
  dispatch({
    type: ActionType.SIGNIN,
    payload: {
      email: userDetails.attributes.email,
      emailVerified: userDetails.attributes.email_verified,
      sub: userDetails.attributes.sub,
    },
  });
};

export const logout = () => (dispatch: Dispatch<Action>): void => {
  dispatch({
    type: ActionType.SIGNOUT,
  });
};
