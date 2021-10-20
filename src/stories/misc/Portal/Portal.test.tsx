import React from 'react';
import { shallow } from 'enzyme';
import Portal from './Portal';

const defaultProps = {
  children: <div id="child">This is the child</div>,
};

const shallowSetup = (props = defaultProps) => {
  const _props = props;
  const wrapper = shallow(<Portal {..._props} />);
  return {
    _props,
    wrapper,
    instance: wrapper.instance(),
  };
};

describe('Portal component', () => {
  it('Renders children', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.find('#child').length).toBe(1);
  });
});
