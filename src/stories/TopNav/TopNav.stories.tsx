import React from 'react';
import { ComponentMeta, Story } from '@storybook/react';
import TopNav from './TopNav';

export default {
  title: 'Components/Composite/TopNav',
  component: TopNav,
  parameters: {
    layout: 'fullscreen',
  },
} as ComponentMeta<typeof TopNav>;

export const Default: Story = () => (
  <TopNav onHome={() => { /* Empty */ }} onLogout={() => { /* Empty */ }} />
);
