import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import Portal from '../Portal/Portal';

export default {
  title: 'Components/Misc/Portal',
  component: Portal,
} as ComponentMeta<typeof Portal>;
const Template: ComponentStory<typeof Portal> = (args) => (
  <div>
    <div id="portal-root-2" />
    <div>
      Should be rendered below this
      <Portal to="portal-root-2" {...args}>
        <div>But it is above</div>
      </Portal>
    </div>
  </div>
);

export const Default = Template.bind({});
Default.args = {};
