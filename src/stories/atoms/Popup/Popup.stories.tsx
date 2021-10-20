import React from 'react';
import { ComponentStory, ComponentMeta, Story } from '@storybook/react';
import Popup from './Popup';
import Button from '../Button/Button';
import Icon from '../Icon/Icon';

export default {
  title: 'Components/Atoms/Popup',
  component: Popup,
} as ComponentMeta<typeof Popup>;
const Template: ComponentStory<typeof Popup> = (args) => <Popup {...args} />;

export const Default = Template.bind({});
Default.args = {
  trigger: <div>Hover me</div>,
  content: 'Hello from Popup!',
};
export const Position: Story = () => (
  <div style={{
    display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gridRowGap: '50px', margin: '50px',
  }}
  >
    <Popup
      trigger={<Button>Top</Button>}
      position="top"
      on="click"
      content="This opens at top"
    />
    <Popup
      trigger={<Button>Top Right</Button>}
      position="top-right"
      on="click"
      content="This opens at top-right"
    />
    <Popup
      trigger={<Button>Centered on the trigger</Button>}
      position="center"
      on="click"
      content="This opens center of the trigger"
    />
    <Popup
      trigger={<Button>Bottom</Button>}
      position="bottom"
      on="click"
      content="This opens at bottom"
    />
    <Popup
      trigger={<Button>Bottom Right</Button>}
      position="bottom-right"
      on="click"
      content="This opens at bottom-right"
    />
    <Popup
      trigger={<Button>Centered on the bottom of trigger</Button>}
      position="center-bottom"
      on="click"
      content="This opens center of the trigger below"
    />
  </div>
);
export const Trigger = Template.bind({});
Trigger.args = {
  trigger: <Icon name="info" />,
  content: 'Icon as a trigger',
  position: 'center-bottom',
};

export const Content: Story = () => (
  <div style={{ display: 'flex', margin: '50px', justifyContent: 'space-evenly' }}>
    <Popup
      trigger={<Button>Content</Button>}
      position="top"
      on="click"
      content="This has some nice content"
    />
    <Popup
      trigger={<Button>Children</Button>}
      position="top"
      on="click"
    ><Button onClick={() => { /* empty */ }}>Please Click me again</Button>
    </Popup>
  </div>
);
