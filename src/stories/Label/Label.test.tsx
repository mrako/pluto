import React from 'react';
import { shallow } from 'enzyme';
import Label from './Label';
import { LabelProps } from './types';

const defaultProps: LabelProps = {
  htmlFor: 'input-name',
  text: 'label text',
};

const shallowSetup = (props = defaultProps) => {
  const _props = props;
  const wrapper = shallow(<Label {..._props} />);
  return {
    _props,
    wrapper,
  };
};

describe('Label component', () => {
  it('The component renders', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.text()).toBe('label text');
    expect(wrapper.find('Info').length).toBe(0);
  });

  it('If disabled is passed, the label is disabled', () => {
    const { wrapper } = shallowSetup({ ...defaultProps, disabled: true });
    expect(wrapper.find('label').hasClass('disabled-label')).toBe(true);
  });

  it('if info is not passed, the Info component is not visible', () => {
    const { wrapper } = shallowSetup();
    expect(wrapper.find('Info').length).toBe(0);
  });

  it('if info is passed, the Info component is visible', () => {
    const { wrapper, _props } = shallowSetup({
      ...defaultProps,
      info: 'some input instructions',
    });
    expect(wrapper.find('Info').length).toBe(1);
    expect(wrapper.find('Info').prop('content')).toEqual(_props.info);
  });
});
