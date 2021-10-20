import React from 'react';
import { shallow } from 'enzyme';
import TextArea from './TextArea';
import { TextAreaProps } from './types';

const defaultProps: TextAreaProps = {
  id: 'textarea-id',
  name: undefined,
  placeholder: undefined,
  value: undefined,
  rows: 5,
  disabled: false,
  onChange: undefined,
  defaultValue: undefined,
  className: '',
  fluid: undefined,
};

const shallowSetup = (props = defaultProps) => {
  const _props = props;
  _props.onChange = jest.fn();
  const wrapper = shallow(<TextArea {..._props} />);
  return {
    _props,
    wrapper,
    instance: wrapper.instance(),
  };
};

describe('TextArea component', () => {
  it('Renders TextArea component', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find('fluid').length).toBe(0);
    expect(wrapper.find('textarea').prop('id')).toBe('textarea-id');
    expect(wrapper.find('textarea').prop('rows')).toBe(5);
  });

  it('Test that textarea change works', () => {
    const { _props, wrapper } = shallowSetup({ ...defaultProps });
    wrapper.find('textarea').simulate('change', { value: 'textarea value' });
    expect(_props.onChange).toHaveBeenCalledTimes(1);
    expect(_props.onChange).toHaveBeenCalledWith({ value: 'textarea value' });
  });

  it('If disabled is passed, the button is dissabled', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, disabled: true });
    expect(wrapper.find('textarea').prop('disabled')).toBe(true);
    expect(wrapper.find('textarea').hasClass('disabled-textarea')).toBe(true);
  });

  it('Custom classname is visible, if passed', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, className: 'test-class' });
    expect(wrapper.find('textarea').hasClass('test-class')).toBe(true);
  });

  it('Fluid prop gets turned into class', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, fluid: true });
    expect(wrapper.hasClass('fluid')).toBe(true);
  });

  describe('Error handling', () => {
    it('if error is passed, the input turns red', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, error: true });
      expect(wrapper.hasClass('error-wrapper')).toBe(true);
      expect(wrapper.find('textarea').hasClass('error-outline')).toBe(true);
    });

    it('if error message is passed, it shows it under the textarea', () => {
      const { wrapper } = shallowSetup({ ...defaultProps, error: 'Error message' });
      expect(wrapper.hasClass('error-wrapper')).toBe(true);
      expect(wrapper.find('.error').length).toBe(1);
      expect(wrapper.find('.error').text()).toBe('Error message');
    });
  });
});
