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
    if (installationId && setupAction === 'install' && user) {
      dispatch(bindPlutoUserToProject(installationId, user.sub));
    }
  }, [queryParams, dispatch, user]);
  return (
    <Redirect to="/home" />
  );
}
