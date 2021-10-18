import React from 'react';
import { shallow } from 'enzyme';
import TopNav from './TopNav';

const onLogout = jest.fn();
const onHome = jest.fn();
describe('TopNav', () => {
  it('calls onLogout when clicking Logout Button', () => {
    const wrapper = shallow(<TopNav onLogout={onLogout} onHome={onHome} />);
    expect(wrapper.find('Button')).toHaveLength(1);
    wrapper.find('Button').simulate('click');
    expect(onLogout).toHaveBeenCalledTimes(1);
  });
  it('calls onLogout when clicking Home', () => {
    const wrapper = shallow(<TopNav onLogout={onLogout} onHome={onHome} />);
    expect(wrapper.find('.home')).toHaveLength(1);
    wrapper.find('.home').simulate('click');
    expect(onHome).toHaveBeenCalledTimes(1);
  });
  it('renders <nav> and a below <div>', () => {
    const wrapper = shallow(<TopNav onLogout={onLogout} onHome={onHome} />);
    const fragment = wrapper.find('Fragment');
    expect(wrapper.find('nav').parent()).toEqual(fragment);
    expect(wrapper.find('.below').parent()).toEqual(fragment);
  });
});
