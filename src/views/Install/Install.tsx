import React, { ReactElement, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
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

// ?code=99df1dc7e416828d26b5&installation_id=20183266&setup_action=install
// https://github.com/apps/pluto-application/installations/new/permissions?target_id=83220112&state=1b23
