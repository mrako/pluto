import React, { ReactElement, useCallback, useEffect } from 'react';
import { useHistory } from 'react-router';
import { useAppSelector, useAppDispatch } from 'utils';

import Card from 'stories/composite/Card/Card';
import * as projectActions from 'store/actions/projectActions';

import './Home.css';

export default function Home(): ReactElement {
  const projects = useAppSelector((state) => state.project.projects);
  const loading = useAppSelector((state) => state.project.loading);
  const history = useHistory();
  const dispatch = useAppDispatch();

  const newProject = useCallback(() => {
    history.push('/project/create');
  }, [history]);

  const goToProject = useCallback((uuid) => {
    history.push(`/project/${uuid}`);
  }, [history],
  );
  const installApp = useCallback(() => {
    window.location.href = process.env.REACT_APP_GITHUB_APP_INSTALLATION_URL as string;
  }, []);

  useEffect(() => {
    dispatch(projectActions.GetProjectsAction());
  }, [dispatch]);

  return (
    <div className="home-container">
      <h2>Welcome to Pluto</h2>
      <div className="home-cards">
        <Card
          id="new-project"
          title="Create new project"
          subtitle="You can create a new project and repository effortlessly using our ready made templates"
          action={newProject}
          actionTitle="Create New Project"
        />
        <Card
          id="install-pluto-app"
          title="Install Pluto App"
          subtitle="Install Pluto Github app"
          action={installApp}
          actionTitle="Install"
        />
      </div>
      <h2>Projects</h2>
      <div className="home-projects">
        {loading ? 'Loading...' : projects.map((project):ReactElement => (
          <Card
            key={project.uuid}
            id={`${project.name}-card`}
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
