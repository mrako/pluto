import React, { ReactElement } from 'react';
import Button from 'stories/atoms/Button/Button';
import Input from 'stories/atoms/Input/Input';
import TextArea from 'stories/atoms/TextArea/TextArea';

interface Props {
  error: null | string,
  onChangeHandler: React.ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement>,
  loading: boolean,
  onSubmit: () => void;
  fieldDefaultValues: {
    name: string,
    description: string,
    repository: string,
    githubToken: string,
  }
}

export default function CreateProjectForm({
  error, onChangeHandler, loading, onSubmit, fieldDefaultValues,
} : Props):ReactElement {
  return (
    <div className="project-container">
      <div className="project-form">
        <div className="project-error">{error}</div>
        <h2 className="project-form-title">Create new project</h2>
        <Input
          className="project-form-input"
          fluid
          defaultValue={fieldDefaultValues.name}
          name="name"
          onChange={onChangeHandler}
          id="name"
          placeholder="Project name"
          label="Project name"
        />
        <TextArea
          className="project-form-input"
          rows={2}
          defaultValue={fieldDefaultValues.description}
          name="description"
          onChange={onChangeHandler}
          id="description"
          placeholder="Project description"
          label="Project description"
        />
        <Input
          className="project-form-input"
          fluid
          defaultValue={fieldDefaultValues.repository}
          name="repository"
          onChange={onChangeHandler}
          placeholder="Repository name"
          id="repository"
          label="Repository name"
        />
        <TextArea
          className="project-form-input"
          rows={2}
          defaultValue={fieldDefaultValues.githubToken}
          name="githubToken"
          onChange={onChangeHandler}
          id="github-token"
          placeholder="Github Personal Access Token"
          label="Github Personal Access Token"
          info={`This will only be used to create the repositories and push the templates to them.
          This will not be stored in any way`}
        />
        <Button loading={loading} onClick={onSubmit} id="create">CREATE</Button>
      </div>
    </div>
  );
}
