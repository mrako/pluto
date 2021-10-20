import React from 'react';
import { ComponentMeta, Story } from '@storybook/react';
import PageContent from './PageContent';

export default {
  title: 'Components/Composite/PageContent',
  component: PageContent,
  parameters: {
    layout: 'fullscreen',
  },
} as ComponentMeta<typeof PageContent>;

export const Default: Story = () => (
  <PageContent>Content goes here</PageContent>
);
