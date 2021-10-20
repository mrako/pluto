import { ReactNode, ReactPortal, useEffect } from 'react';
import { createPortal } from 'react-dom';

interface PortalProps {
  /** ID of element to render the children. If not passed will render them under document body */
  to?: string,
  children: ReactNode,
}
export default function Portal({ to, children }: PortalProps): ReactPortal {
  const el = document.createElement('div');
  useEffect(() => {
    const portalRoot = to ? document.getElementById(to) : document.getElementsByTagName('BODY')[0];
    if (portalRoot) {
      portalRoot.appendChild(el);
    }
    return () => {
      if (portalRoot) {
        portalRoot.removeChild(el);
      }
    };
  }, [to, el]);
  return createPortal(children, el);
}
