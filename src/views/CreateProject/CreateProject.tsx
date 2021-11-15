import React, {
  ReactElement, useState, useCallback, ChangeEvent,
} from 'react';
import { useHistory } from 'react-router';
import * as projectActions from 'store/actions/projectActions';
import { useAppSelector, useAppDispatch } from 'utils';
import CreateProjectForm from './CreateProjectForm/CreateProjectForm';
import CreateProjectStatus, { LoadingStateStatus } from './CreateProjectStatus/CreateProjectStatus';

import './CreateProject.css';

const initialLoadingState: LoadingStateStatus = {
  name: '',
  status: 'loading',
};

export default function Project(): ReactElement {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [repository, setRepository] = useState('');
  const [githubToken, setGithubToken] = useState('');
  /* const [template, setTemplate] = useState('Python Application'); */

  const [submitting, setSubmitting] = useState(false);
  const [projectLoadingState, setProjectLoadingState] = useState(initialLoadingState);
  const [repositoryLoadingState, setRepositoryLoadingState] = useState(initialLoadingState);
  const [createdProject, setCreatedProject] = useState('');
  const dispatch = useAppDispatch();
  const loading = useAppSelector((state) => state.project.loading);
  const error = useAppSelector((state) => state.project.error);
  const history = useHistory();

  const onChangeHandler = useCallback((event: ChangeEvent<HTMLInputElement> | ChangeEvent<HTMLTextAreaElement>) => {
    switch (event.target.name) {
      case 'name':
        setName(event.target.value);
        break;
      case 'description':
        setDescription(event.target.value);
        break;
      case 'repository':
        setRepository(event.target.value);
        break;
      case 'githubToken':
        setGithubToken(event.target.value);
        break;
        /* case 'template':
        setTemplate(event.target.value); */
        break;
      default:
        break;
    }
  }, []);

  const onSubmit = async (): Promise<void> => {
    setProjectLoadingState({ name, status: 'loading' });
    setRepositoryLoadingState({ name: repository, status: 'loading' });
    setSubmitting(true);
    dispatch(projectActions.CreateProjectAction(name, description))
      .then((projectUuid) => {
        setCreatedProject(projectUuid);
        setProjectLoadingState({ name, status: 'success' });
        dispatch(projectActions.createRepositoryAction(repository, githubToken, projectUuid))
          .then(() => {
            setRepositoryLoadingState({ name: repository, status: 'success' });
          })
          .catch((error) => {
            setRepositoryLoadingState({ name: repository, status: 'failure', error });
          });
      })
      .catch((error) => {
        setProjectLoadingState({ name, status: 'failure', error });
      });
  };

  const goToProject = useCallback(() => {
    history.push(`/project/${createdProject}`);
  }, [history, createdProject]);

  return (
    submitting ? <CreateProjectStatus goBack={() => setSubmitting(false)} goToProject={goToProject} project={projectLoadingState} repository={repositoryLoadingState} /> : (
      <CreateProjectForm
        fieldDefaultValues={{
          name,
          description,
          repository,
          githubToken,
        }}
        onSubmit={onSubmit}
        error={error}
        onChangeHandler={onChangeHandler}
        loading={loading}
      />
    )

  );
}
