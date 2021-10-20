import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Label from './Label';

export default {
  title: 'Components/Atoms/Label',
  component: Label,
} as ComponentMeta<typeof Label>;

const Template: ComponentStory<typeof Label> = (args) => <Label {...args}></Label>;

export const Default = Template.bind({});
Default.args = {
  text: 'This is a Label',
};

export const WithInfo = Template.bind({});
WithInfo.args = {
  text: 'This is a Label',
  info: 'Info here!',
};
