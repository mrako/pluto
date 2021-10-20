import React, { ReactElement, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useAppSelector } from 'utils';
import * as projectActions from 'store/actions/projectActions';
import { useRouteMatch } from 'react-router-dom';

export default function Project(): ReactElement {
  const dispatch = useDispatch();
  const match = useRouteMatch<{uuid: string}>();
  useEffect(() => {
    dispatch(projectActions.GetProjectByUUID(match.params.uuid));
    return () => {
      dispatch(projectActions.ClearCurrentProject());
    };
  }, [dispatch, match.params.uuid]);
  const loading = useAppSelector((state) => state.project.loading);
  const project = useAppSelector((state) => state.project.currentProject);

  return (
    <div>
      {loading ? 'Loading...'
        : (
          <div>
            {project?.name}
          </div>
        )}

    </div>
  );
}