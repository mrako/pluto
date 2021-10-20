import { ReactElement } from 'react';

export interface PopupProps {
  on?: 'hover' | 'click',
  /** Where the popup appears */
  position?: 'top' | 'top-right' | 'bottom' | 'bottom-right' | 'center' | 'center-bottom',
  /** Element to be triggered */
  trigger: ReactElement,
  /** use this for simple text popups */
  content?: string,
  /** Custom CSS classes when using content */
  contentClasses?: string,
  /** Custon CSS classes for the whole */
  className?: string,
  /** Use this for more complex than simple text popups */
  children?: ReactElement,
  /** x Offset of the popup in pixels */
  xOffset?: number,
  /** y Offset of the popup in pixels */
  yOffset?: number,
  /** id of the popup */
  id?: string,
  /** Removes all borders and shadows so that it's easier to create custom popup */
  borderless?: boolean,
}
