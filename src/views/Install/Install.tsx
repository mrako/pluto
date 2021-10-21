import React, { ReactElement, useEffect } from 'react';
// import { Redirect } from 'react-router-dom';
import { useQuery } from 'utils';

export default function Install(): ReactElement {
  const queryParams = useQuery();
  useEffect(() => {
    if (queryParams.get('installation_id') && queryParams.get('setup_action') === 'install') {
      console.log('something here');
    }
  }, [queryParams]);
  return (
    <div>
      {queryParams.get('installation_id')}
      {queryParams.get('setup_action')}
    </div>
    /* <Redirect to="/home" state: { from: routeProps.location } }/> */
  );
}
