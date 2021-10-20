import { Dispatch } from 'redux';
import { API } from 'aws-amplify';
import { createProjectMutation } from 'graphql/mutations';
import { getProjectByUUIDQuery, getProjectsQuery } from 'graphql/queries';
import { IProject } from 'types/types';
import history from 'customHistory';
import { ActionType, Action } from '../actionTypes';

const apiName = 'api';
const path = '/api';
const headers = {
  'content-type': 'application/json',
  Accept: 'application/json',
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function checkErrors(response: any, dataName: string) {
  if (response.data[dataName].errors) {
    throw response.data[dataName].errors;
  }
}

function getErrorString(error: unknown): string {
  if (typeof error === 'string') {
    return error;
  } else if (error instanceof Error) {
    return error.message;
  } else if (error instanceof Array) {
    return error.toString();
  }
  return 'Error occured';
}
export const CreateProjectAction = (name: string, description: string) => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.PROJECTS_LOADING });
  const request = {
    headers,
    body: { query: createProjectMutation(name, description) },
  };
  try {
    const response = await API.post(apiName, path, request);
    checkErrors(response, 'createProject');
    const projectUUID: string = response.data?.createProject?.project?.uuid;
    dispatch({
      type: ActionType.CREATE_PROJECT_SUCCESS,
    });
    history.push(`/project/${projectUUID}`);
  } catch (error) {
    const errorString = getErrorString(error);
    dispatch({
      type: ActionType.CREATE_PROJECT_FAILED,
      payload: errorString,
    });
  }
};

export const GetProjectsAction = () => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.PROJECTS_LOADING });
  const request = {
    headers,
    body: { query: getProjectsQuery() },
  };
  try {
    const response = await API.post(apiName, path, request);
    checkErrors(response, 'projects');
    const projectsResponse: IProject[] = response.data?.projects?.projects;
    dispatch({
      type: ActionType.GET_PROJECTS_SUCCESS,
      payload: projectsResponse,
    });
  } catch (error) {
    const errorString = getErrorString(error);
    dispatch({
      type: ActionType.GET_PROJECTS_FAILED,
      payload: errorString,
    });
  }
};

export const GetProjectByUUID = (uuid:string) => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.PROJECTS_LOADING });
  const request = {
    headers,
    body: { query: getProjectByUUIDQuery(uuid) },
  };
  try {
    const response = await API.post(apiName, path, request);
    checkErrors(response, 'project');
    const projectsResponse: IProject = response.data?.project?.project;
    dispatch({
      type: ActionType.GET_CURRENT_PROJECT_SUCCESS,
      payload: projectsResponse,
    });
  } catch (error) {
    const errorString = getErrorString(error);
    dispatch({
      type: ActionType.GET_CURRENT_PROJECT_FAILED,
      payload: errorString,
    });
  }
};

export const ClearCurrentProject = () => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.CLEAR_CURRENT_PROJECT });
};