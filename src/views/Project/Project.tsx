import React, { ReactElement, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useAppSelector } from 'utils';
import * as projectActions from 'store/actions/projectActions';
import { useRouteMatch } from 'react-router-dom';
import Card from 'stories/composite/Card/Card';
import Spinner from 'stories/atoms/Spinner/Spinner';

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

  function goToRepo(repoUrl:string) {
    window.location = repoUrl as unknown as Location;
  }
  return (
    <div>
      {loading ? <Spinner />
        : (
          <>
            <h1>{project?.name}</h1>
            <h3>Project Description</h3>
            <p>{project?.description}</p>
            <h3>Repositories</h3>
            {project?.repositories?.map((repo) => (
              <Card key={repo.uuid} title={repo.name} subtitle={repo.description} action={() => goToRepo(repo.url)} actionTitle="View Repository" />
            ))}
          </>
        )}

    </div>
  );
}
