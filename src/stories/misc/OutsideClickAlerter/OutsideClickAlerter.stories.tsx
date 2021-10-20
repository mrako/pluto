import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Button from 'stories/atoms/Button/Button';
import OutsideClickAlerter from './OutsideClickAlerter';

export default {
  title: 'Components/Misc/OutsideClickAlerter',
  component: OutsideClickAlerter,
} as ComponentMeta<typeof OutsideClickAlerter>;
const Template: ComponentStory<typeof OutsideClickAlerter> = (args) => (
  <OutsideClickAlerter {...args}><Button onClick={() => { console.log('inside'); }}>Click inside</Button></OutsideClickAlerter>);

export const Default = Template.bind({});
Default.args = {
  onOutsideClick: () => {
    console.log('clicked outside');
  },
};
