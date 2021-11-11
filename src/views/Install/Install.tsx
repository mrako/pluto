import React, { ReactElement, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { bindPlutoUserToProject } from 'store/actions/projectActions';
import { Redirect } from 'react-router-dom';
import { useAppSelector, useQuery } from 'utils';

export default function Install(): ReactElement {
  const queryParams = useQuery();
  const dispatch = useDispatch();
  const user = useAppSelector((state) => state.auth.user);
  useEffect(() => {
    const installationId = queryParams.get('installation_id');
    const setupAction = queryParams.get('setup_action');
    const code = queryParams.get('code');
    if (installationId && setupAction === 'install' && code && user) {
      dispatch(bindPlutoUserToProject(installationId, user.sub, code));
    }
  }, [queryParams, dispatch, user]);
  return (
    <Redirect to="/home" />
  );
}
