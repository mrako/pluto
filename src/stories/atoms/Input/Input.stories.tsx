import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Input from './Input';

export default {
  title: 'Components/Atoms/Input',
  component: Input,
  argTypes: {
    type: {
      options: ['text', 'password', 'email', 'number'],
      control: { type: 'radio' },
    },
  },
} as ComponentMeta<typeof Input>;

const Template: ComponentStory<typeof Input> = (args) => <Input {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  variant: 'primary',
  placeholder: 'Primary variant',
};

export const Secondary = Template.bind({});
Secondary.args = {
  variant: 'secondary',
  placeholder: 'Secondary variant',
};

export const WithDebounce = Template.bind({});
WithDebounce.args = {
  debounceTimer: 300,
  placeholder: 'onChange will fire in 300ms',
};
export const WithIcon = Template.bind({});
WithIcon.args = {
  icon: 'search',
  placeholder: 'Search icon',
};

export const WithLabel = Template.bind({});
WithLabel.args = {
  label: 'This is the label',
  placeholder: 'With label',
  info: 'And here is the info',
};
