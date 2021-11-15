import React, { ReactElement, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { bindPlutoUserToProject } from 'store/actions/projectActions';
import { Redirect } from 'react-router-dom';
import { useQuery } from 'utils';

export default function Install(): ReactElement {
  const queryParams = useQuery();
  const dispatch = useDispatch();
  useEffect(() => {
    const installationId = queryParams.get('installation_id');
    const setupAction = queryParams.get('setup_action');
    const code = queryParams.get('code');
    if (installationId && setupAction === 'install' && code) {
      dispatch(bindPlutoUserToProject(installationId, code));
    }
  }, [queryParams, dispatch]);
  return (
    <Redirect to="/home" />
  );
}
