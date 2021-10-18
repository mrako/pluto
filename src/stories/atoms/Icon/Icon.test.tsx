import React from 'react';
import { shallow } from 'enzyme';
import Icon from './Icon';

describe('Icon', () => {
  it('sets width and height when using shorthand size is mini', () => {
    const wrapper = shallow(<Icon name="edit" size="mini" />);
    expect(wrapper.find({ width: 10 }).length).toBe(1);
    expect(wrapper.find({ height: 10 }).length).toBe(1);
  });
  it('sets width and height when using shorthand size is tiny', () => {
    const wrapper = shallow(<Icon name="edit" size="tiny" />);
    expect(wrapper.find({ width: 12 }).length).toBe(1);
    expect(wrapper.find({ height: 12 }).length).toBe(1);
  });
  it('sets width and height when using shorthand size is small', () => {
    const wrapper = shallow(<Icon name="edit" size="small" />);
    expect(wrapper.find({ width: 16 }).length).toBe(1);
    expect(wrapper.find({ height: 16 }).length).toBe(1);
  });
  it('sets width and height when using shorthand size is medium', () => {
    const wrapper = shallow(<Icon name="edit" size="medium" />);
    expect(wrapper.find({ width: 28 }).length).toBe(1);
    expect(wrapper.find({ height: 28 }).length).toBe(1);
  });
  it('sets width and height when using shorthand size is large', () => {
    const wrapper = shallow(<Icon name="edit" size="large" />);
    expect(wrapper.find({ width: 30 }).length).toBe(1);
    expect(wrapper.find({ height: 30 }).length).toBe(1);
  });
  it('sets width and height when using shorthand size is huge', () => {
    const wrapper = shallow(<Icon name="edit" size="huge" />);
    expect(wrapper.find({ width: 33 }).length).toBe(1);
    expect(wrapper.find({ height: 33 }).length).toBe(1);
  });
  it('sets width and height when using shorthand size is massive', () => {
    const wrapper = shallow(<Icon name="edit" size="massive" />);
    expect(wrapper.find({ width: 36 }).length).toBe(1);
    expect(wrapper.find({ height: 36 }).length).toBe(1);
  });
  it('prefers width and height prop over size', () => {
    const wrapper = shallow(<Icon name="edit" size="huge" width={21} height={54} />);
    expect(wrapper.find({ width: 21 }).length).toBe(1);
    expect(wrapper.find({ height: 54 }).length).toBe(1);
  });
  it('using size and width will set the width to width and height according to size', () => {
    const wrapper = shallow(<Icon name="edit" size="huge" width={21} />);
    expect(wrapper.find({ width: 21 }).length).toBe(1);
    expect(wrapper.find({ height: 33 }).length).toBe(1);
  });
  it('using size and height will set the height to height and width according to size', () => {
    const wrapper = shallow(<Icon name="edit" size="huge" height={21} />);
    expect(wrapper.find({ width: 33 }).length).toBe(1);
    expect(wrapper.find({ height: 21 }).length).toBe(1);
  });
  it('renders null if no name given', () => {
    const wrapper = shallow(<Icon />);
    expect(wrapper.isEmptyRender()).toBe(true);
  });
  it('The color of the icon by default is black', () => {
    const wrapper = shallow(<Icon name="edit" />);
    expect(wrapper.hasClass('black')).toBeTruthy();
  });
  it('render color, if prop is passed', () => {
    const wrapper = shallow(<Icon name="edit" color="primary" />);
    expect(wrapper.hasClass('primary')).toBeTruthy();
  });
});
