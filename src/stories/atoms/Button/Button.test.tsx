import React from 'react';
import { shallow } from 'enzyme';
import Button from './Button';

describe('Button', () => {
  it('renders button', () => {
    const wrapper = shallow(<Button>Hello</Button>);
    expect(wrapper.find('button').length).toBe(1);
  });
  it('gets class fluid if fluid prop is set', () => {
    const wrapper = shallow(<Button fluid>Hello</Button>);
    expect(wrapper.find('button').hasClass('fluid')).toBeTruthy();
  });
  describe('variant', () => {
    it('renders primary variant correctly', () => {
      const wrapper = shallow(<Button variant="primary">Hello</Button>);
      expect(wrapper.find('button').hasClass('btn-primary')).toBe(true);
    });
    it('renders primary secondary correctly', () => {
      const wrapper = shallow(<Button variant="secondary">Hello</Button>);
      expect(wrapper.find('button').hasClass('btn-secondary')).toBe(true);
    });
    it('renders link variant correctly', () => {
      const wrapper = shallow(<Button variant="link">Hello</Button>);
      expect(wrapper.find('button').hasClass('btn-link')).toBe(true);
    });
    it('renders variant even when loading', () => {
      const wrapper = shallow(<Button variant="link" loading>Hello</Button>);
      expect(wrapper.find('button').hasClass('btn-link')).toBe(true);
      expect(wrapper.find('button').hasClass('btn-loading')).toBe(true);
    });
  });
  it('renders loading when loading is true', () => {
    const wrapper = shallow(<Button loading>Hello</Button>);
    expect(wrapper.find('button').hasClass('btn-loading')).toBe(true);
    expect(wrapper.find({ className: 'loading-animation' }).length).toBe(1);
  });
  it('can be disabled', () => {
    const wrapper = shallow(<Button disabled>Hello</Button>);
    expect(wrapper.find({ disabled: true })).toEqual(wrapper.find('button'));
  });
  describe('type', () => {
    it('defaults to button', () => {
      const wrapper = shallow(<Button>Hello</Button>);
      expect(wrapper.find({ type: 'button' })).toEqual(wrapper.find('button'));
    });
    it('can be changed to submit', () => {
      const wrapper = shallow(<Button type="submit">Hello</Button>);
      expect(wrapper.find({ type: 'submit' })).toEqual(wrapper.find('button'));
    });
  });
  describe('children', () => {
    it('can render any child', () => {
      const childNode = <div>Hellurei</div>;
      const wrapper = shallow(<Button variant="secondary">{childNode}</Button>);
      expect(wrapper.containsMatchingElement(childNode)).toBe(true);
    });
    it('can render icon on left side of the text', () => {
      const childNode = <div>Hellurei</div>;
      const wrapper = shallow(<Button icon="search" iconPlace="left" variant="secondary">{childNode}</Button>);
      const textWrapper = wrapper.find('.btn-text');
      const icon = wrapper.find('Icon');
      expect(textWrapper.find('Icon').length).toBe(1);
      expect(textWrapper.childAt(0)).toEqual(icon);
      expect(textWrapper.childAt(1).matchesElement(childNode)).toBe(true);
    });
    it('can render icon on right side of the text', () => {
      const childNode = <div>Hellurei</div>;
      const wrapper = shallow(<Button icon="search" iconPlace="right" variant="secondary">{childNode}</Button>);
      const textWrapper = wrapper.find('.btn-text');
      const icon = wrapper.find('Icon');
      expect(textWrapper.find('Icon').length).toBe(1);
      expect(textWrapper.childAt(1)).toEqual(icon);
      expect(textWrapper.childAt(0).matchesElement(childNode)).toBe(true);
    });
  });
  describe('icon', () => {
    it('can render only an icon', () => {
      const wrapper = shallow(<Button icon="search"></Button>);
      expect(wrapper.find('Icon').length).toBe(1);
      expect(wrapper.find('Icon').hasClass('btn-icon-only')).toBe(true);
    });
    it('sets aria-label correcty for the icon', () => {
      const wrapper = shallow(<Button icon="search" ariaIconLabel="hello"></Button>);
      expect(wrapper.find('Icon')).toEqual(wrapper.find({ 'aria-label': 'hello' }));
    });
  });
});
