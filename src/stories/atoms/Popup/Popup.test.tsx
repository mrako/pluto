import React from 'react';
import { shallow } from 'enzyme';
import Popup from './Popup';
import { PopupProps } from './types';

const defaultProps: PopupProps = {
  on: 'hover',
  position: 'top',
  trigger: (<p id="trigger">popup trigger</p>),
};

const triggerRefCords = {
  bottom: 537,
  height: 36,
  left: 249,
  right: 311.78125,
  top: 501,
  width: 62.78125,
  x: 249,
  y: 501,
};

const popupRefCords = {
  bottom: 1385,
  height: 36,
  left: 0,
  right: 123.578125,
  top: 1349,
  width: 123.578125,
  x: 0,
  y: 1349,
};

const shallowSetup = (props = defaultProps) => {
  const _props = props;
  const wrapper = shallow(<Popup {..._props} />);
  return {
    _props,
    wrapper,
    instance: wrapper.instance(),
  };
};

describe('Popup component', () => {
  it('It renders the Popup Component', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.exists()).toBe(true);
  });
  it('renders children when passed and show is true', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, children: (<div>hello</div>) });
    wrapper.find('#trigger').parent().simulate('mouseEnter');
    expect(
      wrapper.find('.popup').containsMatchingElement(
        <div>hello</div>,
      ),
    ).toBeTruthy();
  });
  it('does not render children when show is false', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, children: (<div>hello</div>) });
    expect(
      wrapper.find('.popup').containsMatchingElement(
        <div>hello</div>,
      ),
    ).toBeFalsy();
  });
  it('If content is passed and show is true, show span with popup content', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, content: 'Instructions' });
    wrapper.find('#trigger').parent().simulate('mouseEnter');
    const contentWrapper = wrapper.find('.popup-content');
    expect(contentWrapper.length).toEqual(1);
    expect(contentWrapper.text()).toEqual('Instructions');
  });
  it('If content is passed and show is false, do not show popupContent', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, content: 'Instructions' });
    const contentWrapper = wrapper.find('.popup-content');
    expect(contentWrapper.length).toEqual(0);
  });
  it('Toggle the popup only on hover', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, on: 'hover', content: 'Instructions' });
    expect(wrapper.find('.popup-content').length).toEqual(0);

    wrapper.find('#trigger').parent().simulate('click');
    expect(wrapper.find('.popup-content').length).toEqual(0);

    wrapper.find('#trigger').parent().simulate('mouseenter');
    expect(wrapper.find('.popup-content').length).not.toEqual(0);

    wrapper.find('#trigger').parent().simulate('click');
    expect(wrapper.find('.popup-content').length).not.toEqual(0);

    wrapper.find('#trigger').parent().simulate('mouseleave');
    expect(wrapper.find('.popup-content').length).toEqual(0);
  });
  it('Toggle the popup only on click', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, on: 'click', content: 'Instructions' });
    expect(wrapper.find('.popup-content').length).toEqual(0);
    wrapper.find('#trigger').parent().simulate('mouseenter');
    expect(wrapper.find('.popup-content').length).toEqual(0);
    wrapper.find('#trigger').parent().simulate('mouseleave');
    expect(wrapper.find('.popup-content').length).toEqual(0);

    wrapper.find('#trigger').parent().simulate('click');
    expect(wrapper.find('.popup-content').length).not.toEqual(0);

    wrapper.find('#trigger').parent().simulate('mouseenter');
    expect(wrapper.find('.popup-content').length).not.toEqual(0);
    wrapper.find('#trigger').parent().simulate('mouseleave');
    expect(wrapper.find('.popup-content').length).not.toEqual(0);

    wrapper.find('#trigger').parent().simulate('click');
    expect(wrapper.find('.popup-content').length).toEqual(0);
  });
  it('Adds borderless class when borderless is passed with content', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, borderless: true, content: 'Hellooo' });
    wrapper.find('#trigger').parent().simulate('mouseenter');
    expect(wrapper.find('.borderless').length).toBe(1);
  });
  it('Adds borderless class when borderless is passed with children', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, borderless: true, children: <div>Hellooo</div> });
    wrapper.find('#trigger').parent().simulate('mouseenter');
    expect(wrapper.find('.borderless').length).toBe(1);
  });
  it('renders the contents inside a Portal', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, content: 'hellurei' });
    wrapper.find('#trigger').parent().simulate('mouseenter');
    expect(wrapper.find('Portal').length).toBe(1);
  });
  describe('position prop', () => {
    it('Sets class to top', () => {
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', position: 'top', content: 'Instructions',
      });
      wrapper.find('#trigger').parent().simulate('click');

      expect(wrapper.find('.top').length).toBe(1);
      expect(wrapper.find('.top-right').length).toBe(0);
      expect(wrapper.find('.bottom').length).toBe(0);
      expect(wrapper.find('.bottom-right').length).toBe(0);
    });
    it('Sets class to top-right', () => {
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', position: 'top-right', content: 'Instructions',
      });
      wrapper.find('#trigger').parent().simulate('click');

      expect(wrapper.find('.top').length).toBe(0);
      expect(wrapper.find('.top-right').length).toBe(1);
      expect(wrapper.find('.bottom').length).toBe(0);
      expect(wrapper.find('.bottom-right').length).toBe(0);
    });
    it('Sets class to bottom', () => {
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', position: 'bottom', content: 'Instructions',
      });
      wrapper.find('#trigger').parent().simulate('click');

      expect(wrapper.find('.top').length).toBe(0);
      expect(wrapper.find('.top-right').length).toBe(0);
      expect(wrapper.find('.bottom').length).toBe(1);
      expect(wrapper.find('.bottom-right').length).toBe(0);
    });
    it('Sets class to bottom-right', () => {
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', position: 'bottom-right', content: 'Instructions',
      });
      wrapper.find('#trigger').parent().simulate('click');

      expect(wrapper.find('.top').length).toBe(0);
      expect(wrapper.find('.top-right').length).toBe(0);
      expect(wrapper.find('.bottom').length).toBe(0);
      expect(wrapper.find('.bottom-right').length).toBe(1);
    });
    it('Center sets class to top', () => {
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', position: 'center', content: 'Instructions',
      });
      wrapper.find('#trigger').parent().simulate('click');

      expect(wrapper.find('.top').length).toBe(1);
      expect(wrapper.find('.top-right').length).toBe(0);
      expect(wrapper.find('.bottom').length).toBe(0);
      expect(wrapper.find('.bottom-right').length).toBe(0);
    });
    it('center-bottom Sets class to bottom', () => {
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', position: 'center-bottom', content: 'Instructions',
      });
      wrapper.find('#trigger').parent().simulate('click');

      expect(wrapper.find('.top').length).toBe(0);
      expect(wrapper.find('.top-right').length).toBe(0);
      expect(wrapper.find('.bottom').length).toBe(1);
      expect(wrapper.find('.bottom-right').length).toBe(0);
    });
    it('does not set cordinates when show is false ', () => {
      const getBoundingClientRectMock = jest.fn();
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => getBoundingClientRectMock } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => getBoundingClientRectMock } });
      shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test',
      });
      // wrapper.find('#trigger').parent().simulate('click');
      expect(getBoundingClientRectMock).toHaveBeenCalledTimes(0);
    });
    it('sets cordinates on position top', () => {
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } });
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test', position: 'top',
      });
      wrapper.find('#trigger').parent().simulate('click');
      expect(wrapper.find('.top').length).toBe(1);
      expect(wrapper.find('#test').props().style).toEqual({ left: 249, top: 457 });
    });
    it('sets cordinates on position bottom', () => {
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } });
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test', position: 'bottom',
      });
      wrapper.find('#trigger').parent().simulate('click');
      expect(wrapper.find('.bottom').length).toBe(1);
      expect(wrapper.find('#test').props().style).toEqual({ left: 249, top: 545 });
    });
    it('sets cordinates on position top-right', () => {
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } });
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test', position: 'top-right',
      });
      wrapper.find('#trigger').parent().simulate('click');
      expect(wrapper.find('.top-right').length).toBe(1);
      expect(wrapper.find('#test').props().style).toEqual({ left: 188.203125, top: 457 });
    });
    it('sets cordinates on position bottom-right', () => {
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } });
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test', position: 'bottom-right',
      });
      wrapper.find('#trigger').parent().simulate('click');
      expect(wrapper.find('.bottom-right').length).toBe(1);
      expect(wrapper.find('#test').props().style).toEqual({ left: 188.203125, top: 545 });
    });
    it('sets cordinates on position center', () => {
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } });
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test', position: 'center',
      });
      wrapper.find('#trigger').parent().simulate('click');
      expect(wrapper.find('.top').length).toBe(1);
      expect(wrapper.find('#test').props().style).toEqual({ left: 261.390625, top: 457 });
    });
    it('sets cordinates on position center-bottom', () => {
      jest.spyOn(React, 'useRef')
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => triggerRefCords } })
        .mockReturnValueOnce({ current: { getBoundingClientRect: () => popupRefCords } });
      const { wrapper } = shallowSetup({
        ...defaultProps, on: 'click', content: 'Hello', id: 'test', position: 'center-bottom',
      });
      wrapper.find('#trigger').parent().simulate('click');
      expect(wrapper.find('.bottom').length).toBe(1);
      expect(wrapper.find('#test').props().style).toEqual({ left: 261.390625, top: 545 });
    });
  });
});
