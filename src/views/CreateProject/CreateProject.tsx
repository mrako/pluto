import React, {
  ReactElement, useState, useCallback, ChangeEvent,
} from 'react';
import { useDispatch } from 'react-redux';
import Button from 'stories/atoms/Button/Button';
import Input from 'stories/atoms/Input/Input';
import TextArea from 'stories/atoms/TextArea/TextArea';
import * as projectActions from 'store/actions/projectActions';
import { useAppSelector } from 'utils';

import './CreateProject.css';

export default function Project(): ReactElement {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  /* const [repository, setRepository] = useState('');
  const [template, setTemplate] = useState('Python Application'); */
  const dispatch = useDispatch();
  const loading = useAppSelector((state) => state.project.loading);
  const error = useAppSelector((state) => state.project.error);

  const onChangeHandler = useCallback((event: ChangeEvent<HTMLInputElement> | ChangeEvent<HTMLTextAreaElement>) => {
    switch (event.target.name) {
      case 'name':
        setName(event.target.value);
        break;
      case 'description':
        setDescription(event.target.value);
        break;
        /* case 'repository':
        setRepository(event.target.value);
        break;
      case 'template':
        setTemplate(event.target.value); */
        break;
      default:
        break;
    }
  }, []);

  const onSubmit = async () => {
    await dispatch(projectActions.CreateProjectAction(name, description));
  };

  return (
    <div className="project-container">
      <div className="project-form">
        <div className="project-error">{error}</div>
        <h2 className="project-form-title">Create new project</h2>
        <Input
          className="project-form-input"
          fluid
          name="name"
          onChange={onChangeHandler}
          id="name"
          placeholder="Project name"
          label="Project name"
        />
        <TextArea
          className="project-form-input"
          rows={2}
          name="description"
          onChange={onChangeHandler}
          id="description"
          placeholder="Project description"
          label="Project description"
        />
        <Button loading={loading} onClick={onSubmit} id="create">CREATE</Button>
      </div>
    </div>
  );
}
/* <div>
          <Label text="Repository name" htmlFor="repository" />
          <Input name="repository" onChange={onChangeHandler} id="repository" />
        </div>
        <div>
          <Label text="Repository template" htmlFor="template" />
          <Input name="template" onChange={onChangeHandler} id="template" disabled value="Python application" />
        </div> */
