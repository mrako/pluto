import React from 'react';
import { shallow } from 'enzyme';
import Card from './Card';

const actionMock = jest.fn();
describe('Card', () => {
  it('renders Button if action is given with the text given as actionTitle', () => {
    const wrapper = shallow(<Card title="title" subtitle="subtitle" action={actionMock} actionTitle="buttonTitle" />);
    expect(wrapper.find('Button')).toHaveLength(1);
    expect(wrapper.find('Button').dive().find('button').text()).toEqual('buttonTitle');
  });
  it('fires action when Button is clicked', () => {
    const wrapper = shallow(<Card title="title" subtitle="subtitle" action={actionMock} />);
    wrapper.find('Button').simulate('click');
    expect(actionMock).toHaveBeenCalledTimes(1);
  });
  it('does not render Button if action is absent', () => {
    const wrapper = shallow(<Card title="title" subtitle="subtitle" />);
    expect(wrapper.find('Button')).toHaveLength(0);
  });
  it('renders title and subtitle', () => {
    const wrapper = shallow(<Card title="title" subtitle="subtitle" action={actionMock} />);
    expect(wrapper.find('h2')).toHaveLength(1);
    expect(wrapper.find('h2').text()).toEqual('title');
    expect(wrapper.find('.subtitle').text()).toEqual('subtitle');
  });
  it('renders icon in the title if titleIcon is passed', () => {
    const wrapper = shallow(<Card title="title" subtitle="subtitle" action={actionMock} titleIcon="checkmark" />);
    expect(wrapper.find('Icon')).toHaveLength(1);
    expect(wrapper.find('Icon').parent()).toEqual(wrapper.find('h2'));
  });
});
