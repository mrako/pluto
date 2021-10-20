import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';

import Info from './Info';

export default {
  title: 'Components/Atoms/Info',
  component: Info,
} as ComponentMeta<typeof Info>;

const Template: ComponentStory<typeof Info> = (args) => <div style={{ margin: '30px' }}><Info {...args} /></div>;

export const Default = Template.bind({});
Default.args = {
  content: 'Info!',
};

export const Colors = Template.bind({});
Colors.args = {
  content: 'Info!',
  color: 'primary',
};
