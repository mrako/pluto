import React from 'react';
// import { render, screen } from '@testing-library/react';
import { shallow } from 'enzyme';
import { Auth } from 'aws-amplify';
import PrivateRoute from './PrivateRoute';

const mockDispatch = jest.fn();
jest.mock('react-redux', () => ({
  useSelector: jest.fn(),
  useDispatch: () => mockDispatch,
}));

const mockHistory = {
  push: jest.fn(),
};
jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router');
  return {
    __esModule: true,
    Route: originalModule.Route,
    useHistory: () => mockHistory,
  };
});

jest.mock('aws-amplify', () => ({
  ...jest.requireActual('aws-amplify'),
  Auth: {
    currentSession: jest.fn(),
  },
}));

afterAll(() => {
  jest.restoreAllMocks();
  jest.resetAllMocks();
});

describe('PrivateRoute', () => {
  it('Does not redirect to /login when current session is valid', async () => {
    (Auth.currentSession as jest.Mock).mockReturnValue(Promise.resolve({ isValid: () => true }));
    shallow(<PrivateRoute>testing</PrivateRoute>);
    await Promise.resolve();
    expect(mockHistory.push).toHaveBeenCalledTimes(0);
  });
  it('Redirects to /login when current session is not valid', async () => {
    (Auth.currentSession as jest.Mock).mockReturnValue(Promise.resolve({ isValid: () => false }));
    shallow(<PrivateRoute>testing</PrivateRoute>);
    await Promise.resolve();
    expect(mockHistory.push).toHaveBeenCalledTimes(1);
    expect(mockHistory.push).toHaveBeenCalledWith('/login');
  });
});
