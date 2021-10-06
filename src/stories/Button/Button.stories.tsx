import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Button from './Button';

export default {
  title: 'Components/Atoms/Button',
  component: Button,
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => <Button {...args}></Button>;

export const Primary = Template.bind({});
Primary.args = {
  variant: 'primary',
  children: 'Hello!',
};

export const Secondary = Template.bind({});
Secondary.args = {
  variant: 'secondary',
  children: 'Hello!',
};
export const Link = Template.bind({});
Link.args = {
  variant: 'link',
  children: 'Hello!',
};

export const WithIcon = Template.bind({});
WithIcon.args = {
  variant: 'secondary',
  icon: 'add',
  children: 'Add',
};
