import React, { ReactElement } from 'react';
import Button from 'stories/atoms/Button/Button';
import Icon from 'stories/atoms/Icon/Icon';
import Info from 'stories/atoms/Info/Info';
import Spinner from 'stories/atoms/Spinner/Spinner';

import './CreateProjectStatus.css';

export interface LoadingStateStatus {
  name: string,
  status: 'loading' | 'success' | 'failure',
  error?: string,
}

interface Props {
  project: LoadingStateStatus,
  repository: LoadingStateStatus,
  goToProject: () => void;
  goBack: () => void;
}

export default function CreateProjectStatus({
  project, repository, goToProject, goBack,
}: Props): ReactElement {
  let projectString = 'Initializing Project';
  if (project.status === 'success') {
    projectString = 'Project Initialized';
  } else if (project.status === 'failure') {
    projectString = 'Project Initialization Failed';
  }

  let repositoryString = `Creating Repository: ${repository.name}`;
  if (project.status === 'success' && repository.status === 'loading') {
    repositoryString = `Creating Repository: ${repository.name}`;
  } else if (repository.status === 'success') {
    repositoryString = `Repository ${repository.name} Created`;
  } else if (repository.status === 'failure') {
    repositoryString = `Repository ${repository.name} Creation Failed`;
  }
  return (
    <div className="create-project-status">
      <div className="create-project-status-container">
        <h2>Creating Project</h2>
        <div>
          {project.status === 'loading' ? (
            <div className="loading-status-container">
              <div className="result-spinner">
                <Spinner />
              </div>
              <div>{projectString}</div>
            </div>
          ) : (
            <div className="loading-status-container">
              <div>
                {project.status === 'success'
                  ? <Icon size="small" name="hollowCheckmark" />
                  : <Info icon="warning" size="small" color="black" content={project.error ? project.error : ''} />}
              </div>
              <div className="loading-status-string">
                {projectString}
              </div>
            </div>
          )}
        </div>
        {project.status === 'loading' || project.status === 'failure' ? null : (
          <div className="loading-status-container">
            {repository.status === 'loading' ? (
              <>
                <div className="result-spinner">
                  <Spinner />
                </div>
                <div>{repositoryString}</div>
              </>
            ) : (
              <>
                <div>
                  {repository.status === 'success'
                    ? <Icon size="small" name="hollowCheckmark" />
                    : <Info icon="warning" size="small" color="black" content={repository.error ? repository.error : ''} />}
                </div>
                <div className="loading-status-string">
                  {repositoryString}
                </div>
              </>
            )}
          </div>
        )}

        <div className="loading-status-button">
          {project.status === 'success' && repository.status !== 'loading' ? <Button onClick={goToProject}>Go To Project</Button> : null}
          {project.status === 'failure' ? <Button onClick={goBack}>Back to Form</Button> : null}
        </div>
      </div>
    </div>

  );
}
