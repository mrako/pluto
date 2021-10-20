import React from 'react';
import { shallow } from 'enzyme';
import Input from './Input';
import { InputProps } from './types';

const defaultProps:InputProps = {
  name: 'new-input',
  placeholder: '',
  value: '',
  type: 'text',
  className: '',
  id: 'input id',
  variant: 'primary',
};

const shallowSetup = (props = defaultProps) => {
  const _props = props;
  _props.onChange = jest.fn();
  const wrapper = shallow(<Input {..._props} />);
  return {
    _props,
    wrapper,
    instance: wrapper.instance(),
  };
};

describe('Input component', () => {
  it('The component renders', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.exists()).toBe(true);
  });
  it('Test that input change works', () => {
    const { _props, wrapper } = shallowSetup({ ...defaultProps });
    wrapper.find('input').simulate('change', { value: 'input value' });
    expect(_props.onChange).toHaveBeenCalledTimes(1);
    expect(_props.onChange).toHaveBeenCalledWith({ value: 'input value' });
  });

  it('The component is not disabled by default', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.find('input').prop('disabled')).toBe(undefined);
  });

  it('If disabled is passed, the button is dissabled', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, disabled: true });
    expect(wrapper.find('input').prop('disabled')).toBe(true);
  });

  it('The input can be type password', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, type: 'password' });
    expect(wrapper.find('input').prop('type')).toBe('password');
  });
  it('Primary variant prop gets turned into class', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, variant: 'primary' });
    expect(wrapper.hasClass('primary')).toBe(true);
  });
  it('Secondary variant prop gets turned into class', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, variant: 'secondary' });
    expect(wrapper.hasClass('secondary')).toBe(true);
  });
  it('Fluid prop gets turned into class', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, fluid: true });
    expect(wrapper.hasClass('fluid')).toBe(true);
  });
  it('is debounced when debounceTimer is set', (done) => {
    const { wrapper, _props } = shallowSetup({ ...defaultProps, debounceTimer: 300 });
    const persist = jest.fn();
    wrapper.find('input').simulate('change', { persist, value: 'input value' });
    expect(_props.onChange).toHaveBeenCalledTimes(0);
    setTimeout(() => {
      expect(_props.onChange).toHaveBeenCalledTimes(1);
      expect(_props.onChange).toHaveBeenCalledWith({ value: 'input value', persist });
      expect(persist).toHaveBeenCalledTimes(1);
      done();
    }, 300);
  });
  describe('Icon', () => {
    it('Show icon if icon prop is provided', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, icon: 'add' });
      expect(wrapper.find('Icon').length).toEqual(1);
    });
    it('Do not show icon if icon prop is not provided', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, icon: '' });
      expect(wrapper.find('Icon').length).toEqual(0);
    });
    it('Gets the primary variant coloring class', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, icon: 'add', variant: 'primary' });
      expect(wrapper.find('Icon').hasClass('input-icon-primary')).toBe(true);
    });
    it('Gets the secondary variant coloring class', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, icon: 'add', variant: 'secondary' });
      expect(wrapper.find('Icon').hasClass('input-icon-secondary')).toBe(true);
    });
  });

  describe('Error handling', () => {
    it('if error is passed, the input turns red', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, error: true });
      expect(wrapper.hasClass('error-wrapper')).toBe(true);
      expect(wrapper.find('input').hasClass('error-outline')).toBe(true);
    });

    it('if error message is passed, it shows it under the input', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, error: 'Error message' });
      expect(wrapper.hasClass('error-wrapper')).toBe(true);
      expect(wrapper.find('.error').length).toBe(1);
      expect(wrapper.find('.error').text()).toBe('Error message');
    });
  });
});
