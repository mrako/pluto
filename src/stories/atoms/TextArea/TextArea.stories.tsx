import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import TextArea from './TextArea';

export default {
  title: 'Components/Atoms/TextArea',
  component: TextArea,
} as ComponentMeta<typeof TextArea>;

const Template: ComponentStory<typeof TextArea> = (args) => <TextArea {...args} />;

export const Default = Template.bind({});
Default.args = {
  placeholder: 'Placeholder here',
};

export const WithLabel = Template.bind({});
WithLabel.args = {
  placeholder: 'Placeholder here',
  label: 'This Is the Label',
  info: 'Info goes here',
};
