import React from 'react';
import { shallow } from 'enzyme';
import Info from './Info';
import { InfoProps } from './types';

const defaultProps: InfoProps = {
  content: 'default content prop',
};

const shallowSetup = (props = defaultProps) => {
  const _props = props;
  const wrapper = shallow(<Info {..._props} />);
  return {
    _props,
    wrapper,
  };
};

describe('Info component', () => {
  it('It renders the Popup Component', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('Popup').length).toBe(1);
  });
  it('renders default props for Popup trigger', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.find('Popup')).toHaveLength(1);
    const triggerProps = (wrapper.find('Popup').props() as {trigger: any}).trigger.props;
    expect(triggerProps.color).toEqual('blue');
    expect(triggerProps.size).toEqual('tiny');
    expect(triggerProps.name).toEqual('info');
    expect(triggerProps.className).toEqual(undefined);
    expect(triggerProps.id).toEqual(undefined);
  });
  it('gives correct props to Popup', () => {
    const { wrapper, _props } = shallowSetup();
    expect(wrapper.find('Popup')).toHaveLength(1);
    const wrapperProps: any = wrapper.find('Popup').props();
    expect(wrapperProps.content).toEqual(_props.content);
    expect(wrapperProps.on).toEqual('hover');
    expect(wrapperProps.position).toEqual('center');
  });
  it('renders given props to Popup trigger', () => {
    const { wrapper } = shallowSetup({
      ...defaultProps,
      id: 'hello',
      icon: 'search',
      color: 'white',
      size: 'massive',
      className: 'classy',
    });
    expect(wrapper.find('Popup')).toHaveLength(1);
    const triggerProps = (wrapper.find('Popup').prop('trigger') as {props: any}).props;
    expect(triggerProps.color).toEqual('white');
    expect(triggerProps.size).toEqual('massive');
    expect(triggerProps.name).toEqual('search');
    expect(triggerProps.className).toEqual('classy');
    expect(triggerProps.id).toEqual('hello');
  });
});
