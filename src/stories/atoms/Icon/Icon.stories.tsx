import React from 'react';
import { ComponentStory, ComponentMeta, Story } from '@storybook/react';

import Icon from './Icon';
import { IconName } from './types';

export default {
  title: 'Components/Atoms/Icon',
  component: Icon,
} as ComponentMeta<typeof Icon>;

const Template: ComponentStory<typeof Icon> = (args) => <Icon {...args} />;

export const Default = Template.bind({});
Default.args = {
  name: 'link',
};

const iconsList:IconName[] = ['fullArrowDown', 'fullArrowRight', 'arrowLeft',
  'arrowRight', 'arrowUp', 'arrowDown', 'edit',
  'close', 'cancel', 'delete', 'add', 'backgroundPlus', 'details',
  'link', 'logout', 'checkmark', 'filledCheckmark', 'hollowCheckmark', 'warning', 'info', 'search'];

export const All: Story = () => (
  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr' }}>
    {iconsList.map((iconName) => (
      <div
        key={iconName}
        style={{
          display: 'flex',
          alignItems: 'center',
          margin: '8px 0',
        }}
      >
        <Icon name={iconName} />
        <span style={{ marginLeft: '8px' }}>{iconName}</span>
      </div>
    ))}
  </div>

);
