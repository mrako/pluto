import React from 'react';
// import { render, screen } from '@testing-library/react';
import { shallow } from 'enzyme';
import { Auth } from 'aws-amplify';
import { useHistory } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';

const mockUseDispatch = jest.fn();
jest.mock('react-redux', () => ({
  useSelector: jest.fn(),
  useDispatch: () => mockUseDispatch,
}));

const mockPush = jest.fn();
const mockPath = {
  pathname: '/project/create', search: '', hash: '', state: undefined, key: '2gaabn',
};
jest.mock('react-router-dom', () => {
  const originalModule = jest.requireActual('react-router-dom');
  return {
    __esModule: true,
    Route: originalModule.Route,
    useHistory: () => (
      { push: mockPush }
    ),
    useLocation: () => mockPath,
  };
});

jest.mock('aws-amplify', () => ({
  ...jest.requireActual('aws-amplify'),
  Auth: {
    currentSession: jest.fn(),
  },
}));

describe('PrivateRoute', () => {
  it('Does not redirect to /login when current session is valid', async () => {
    (Auth.currentSession as jest.Mock).mockReturnValue(Promise.resolve({ isValid: () => true }));
    shallow(<PrivateRoute>testing</PrivateRoute>);
    await Promise.resolve();
    expect(useHistory().push).toHaveBeenCalledTimes(0);
  });
  it('Redirects to /login when current session is not valid', async () => {
    (Auth.currentSession as jest.Mock).mockReturnValue(Promise.resolve({ isValid: () => false }));
    shallow(<PrivateRoute>testing</PrivateRoute>);
    await Promise.resolve();
    expect(useHistory().push).toHaveBeenCalledTimes(1);
    expect(useHistory().push).toHaveBeenCalledWith('/login', { from: mockPath });
  });
});
