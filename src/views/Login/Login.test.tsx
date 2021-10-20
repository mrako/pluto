import React from 'react';
import { shallow } from 'enzyme';
import Login from './Login';

const mockDispatch = jest.fn();
jest.mock('react-redux', () => ({
  useSelector: jest.fn(),
  useDispatch: () => mockDispatch,
}));

const mockHistory = {
  push: jest.fn(),
};
jest.mock('react-router-dom', () => ({
  useHistory: () => mockHistory,
}));

describe('Login', () => {
  test('Calls dispatch and history.push on signed in event', () => {
    const wrapper = shallow(<Login />);
    wrapper.prop('handleAuthStateChange')('signedin');
    expect(mockDispatch).toHaveBeenCalledTimes(1);
    expect(mockHistory.push).toHaveBeenCalledTimes(1);
    expect(mockHistory.push).toHaveBeenCalledWith('/home');
  });
  test('Does not call dispatch or history.push on eny other event', () => {
    const wrapper = shallow(<Login />);
    wrapper.prop('handleAuthStateChange')('signedout');
    expect(mockDispatch).toHaveBeenCalledTimes(0);
    expect(mockHistory.push).toHaveBeenCalledTimes(0);
    wrapper.prop('handleAuthStateChange')('signin');
    expect(mockDispatch).toHaveBeenCalledTimes(0);
    expect(mockHistory.push).toHaveBeenCalledTimes(0);
    wrapper.prop('handleAuthStateChange')('nönnönnöö');
    expect(mockDispatch).toHaveBeenCalledTimes(0);
    expect(mockHistory.push).toHaveBeenCalledTimes(0);
  });
});
