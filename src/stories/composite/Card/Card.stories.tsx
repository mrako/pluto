import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Card from './Card';

export default {
  title: 'Components/Composite/Card',
  component: Card,
} as ComponentMeta<typeof Card>;

const Template: ComponentStory<typeof Card> = (args) => <Card {...args}></Card>;

export const Default = Template.bind({});
Default.args = {
  title: 'This is the title',
  subtitle: 'You can give a subtitle for the card like this. If it is really long it will go to second row',
  action: () => { /* */ },
  actionTitle: 'Button title',
};
export const WithIcon = Template.bind({});
WithIcon.args = {
  title: 'This is the title',
  subtitle: 'You can give a subtitle for the card like this. If it is really long it will go to second row',
  action: () => { /* */ },
  actionTitle: 'Button title',
  titleIcon: 'checkmark',
};

export const WithoutAction = Template.bind({});
WithoutAction.args = {
  title: 'This is the title',
  subtitle: 'You can give a subtitle for the card like this. If it is really long it will go to second row',
};
