import React from 'react';
import { shallow } from 'enzyme';
import OutsideClickAlerter from './OutsideClickAlerter';

describe('OutsideClickAlerter', () => {
  const children = <button type="button">Button Text</button>;
  it('renders children', () => {
    const outsideClick = jest.fn();
    const wrapper = shallow(<OutsideClickAlerter onOutsideClick={outsideClick}>{children}</OutsideClickAlerter>);
    expect(wrapper.find('button').getElement()).toEqual(children);
  });
});
