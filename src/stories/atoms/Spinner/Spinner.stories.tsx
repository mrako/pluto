import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Spinner from './Spinner';

export default {
  title: 'Components/Atoms/Spinner',
  component: Spinner,
} as ComponentMeta<typeof Spinner>;

const Template: ComponentStory<typeof Spinner> = (args) => <Spinner {...args} />;

export const Default = Template.bind({});

export const Inverted = Template.bind({});
Inverted.args = {
  inverted: true,
};