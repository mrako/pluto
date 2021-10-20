import React, { ReactElement, useCallback, useEffect } from 'react';
import { useHistory } from 'react-router';
import { useDispatch } from 'react-redux';
import { useAppSelector } from 'utils';

import Card from 'stories/composite/Card/Card';
import * as projectActions from 'store/actions/projectActions';

import './Home.css';

export default function Home(): ReactElement {
  const projects = useAppSelector((state) => state.project.projects);
  const loading = useAppSelector((state) => state.project.loading);
  const history = useHistory();
  const dispatch = useDispatch();

  const newProject = useCallback(() => {
    history.push('/project/create');
  }, [history]);

  const goToProject = useCallback((uuid) => {
    history.push(`/project/${uuid}`);
  }, [history],
  );

  useEffect(() => {
    dispatch(projectActions.GetProjectsAction());
  }, [dispatch]);

  return (
    <div className="home-container">
      <h2>Welcome to Pluto</h2>
      <div className="home-cards">
        <Card
          title="Create new project"
          subtitle="You can create a new project and repository effortlessly using our ready made templates"
          action={newProject}
          actionTitle="Create New Project"
        />
        <Card
          title="Install Pluto App"
          subtitle="You have installed the Pluto Github App successfully!"
          titleIcon="checkmark"
        />
      </div>
      <h2>Projects</h2>
      <div className="home-projects">
        {loading ? 'Loading...' : projects.map((project):ReactElement => (
          <Card
            key={project.uuid}
            title={project.name}
            subtitle={project.description}
            action={() => goToProject(project.uuid)}
            actionTitle="View project"
          />
        ))}
      </div>
    </div>
  );
}
