import React, { ReactElement, ReactNode } from 'react';
import './PageContent.css';

interface PageContentProps {
  children: ReactNode,
}
export default function PageContent({ children }: PageContentProps): ReactElement {
  return (
    <div className="page-content">
      {children}
    </div>
  );
}
