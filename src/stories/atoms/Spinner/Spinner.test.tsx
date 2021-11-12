import React from 'react';
import { shallow } from 'enzyme';
import Spinner from './Spinner';

const shallowSetup = (props = {}) => {
  const _props = props;
  const wrapper = shallow(<Spinner {..._props} />);
  return {
    _props,
    wrapper,
  };
};

describe('Spinner', () => {
  it('renders div as the root element', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.find('div').first()).toEqual(wrapper);
  });
  it('has class spinner', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.find('.spinner')).toEqual(wrapper);
  });
  it('assigns class inverted to root div when inverted prop is passed', () => {
    const { wrapper } = shallowSetup({ inverted: true });
    expect(wrapper.find('.spinner.inverted')).toEqual(wrapper);
  });
});
