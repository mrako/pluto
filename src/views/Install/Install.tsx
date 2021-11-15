import React, { ReactElement, useEffect, useState } from 'react';
import { bindPlutoUserToProject } from 'store/actions/projectActions';
import { Redirect } from 'react-router-dom';
import { useQuery, useAppDispatch } from 'utils';
import Spinner from 'stories/atoms/Spinner/Spinner';

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export default function Install(): ReactElement {
  const queryParams = useQuery();
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const installationId = queryParams.get('installation_id');
    const setupAction = queryParams.get('setup_action');
    const code = queryParams.get('code');
    // TODO: Make the retrying better
    if (installationId && setupAction === 'install' && code) {
      dispatch(bindPlutoUserToProject(installationId, code))
        .catch(() => {
          sleep(1000).then(() => {
            dispatch(bindPlutoUserToProject(installationId, code))
              .catch(() => {
                sleep(1000).then(() => {
                  dispatch(bindPlutoUserToProject(installationId, code));
                });
              });
          });
        }).finally(() => {
          setLoading(false);
        });
    }
  }, [queryParams, dispatch]);
  return (
    loading ? <Spinner /> : <Redirect to="/home" />
  );
}
