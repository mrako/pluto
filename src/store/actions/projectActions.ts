import { Dispatch } from 'redux';
import { API } from 'aws-amplify';
import { createProjectMutation, bindUserToProjectMutation, createRepositoryMutation } from 'graphql/mutations';
import { getProjectByUUIDQuery, getProjectsQuery, getUserLinksQuery } from 'graphql/queries';
import { IProject } from 'types/types';
import history from 'customHistory';
import store from 'store/configureStore';
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
    if (error.message === 'Request failed with status code 401') {
      history.push('/login', { from: history.location });
    }
    return error.message;
  } else if (error instanceof Array) {
    return error.toString();
  }
  return 'Error occured';
}

export const createRepositoryAction = (name: string, token: string, projectUUID: string) => async (dispatch: Dispatch<Action>): Promise<void | string> => {
  const request = {
    headers: { ...headers, Authorization: `Bearer ${store.getState().auth.user?.token}` },
    body: { query: createRepositoryMutation(name, projectUUID, token) },
  };
  try {
    const response = await API.post(apiName, path, request);
    checkErrors(response, 'createRepository');
    dispatch({
      type: ActionType.CREATE_REPOSITORY_SUCCESS,
    });
  } catch (error) {
    const errorString = getErrorString(error);
    dispatch({
      type: ActionType.CREATE_REPOSITORY_FAILED,
      payload: errorString,
    });
    return Promise.reject(errorString);
  }
  return Promise.resolve();
};

export const CreateProjectAction = (name: string, description: string) => async (dispatch: Dispatch<Action>): Promise<string> => {
  dispatch({ type: ActionType.PROJECTS_LOADING });

  const userLinksRequest = {
    headers: { ...headers, Authorization: `Bearer ${store.getState().auth.user?.token}` },
    body: { query: getUserLinksQuery() },
  };
  try {
    const userLinks = await API.post(apiName, path, userLinksRequest);
    checkErrors(userLinks, 'userLinks');
    // TODO: Give the userlink UUID as function parameter (ask the user which org/user to create the repos)
    const userLink: string = userLinks.data?.userLinks.links[0].uuid;
    const request = {
      headers: { ...headers, Authorization: `Bearer ${store.getState().auth.user?.token}` },
      body: { query: createProjectMutation(name, description, userLink) },
    };

    const response = await API.post(apiName, path, request);
    checkErrors(response, 'createProject');
    const projectUUID: string = response.data?.createProject?.project?.uuid;
    dispatch({
      type: ActionType.CREATE_PROJECT_SUCCESS,
    });
    return Promise.resolve(projectUUID);
  } catch (error) {
    const errorString = getErrorString(error);
    dispatch({
      type: ActionType.CREATE_PROJECT_FAILED,
      payload: errorString,
    });
    return Promise.reject(errorString);
  }
};

export const GetProjectsAction = () => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.PROJECTS_LOADING });
  const request = {
    headers: { ...headers, Authorization: `Bearer ${store.getState().auth.user?.token}` },
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
    return Promise.reject();
  }
  return Promise.resolve();
};

export const GetProjectByUUID = (uuid:string) => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.PROJECTS_LOADING });
  const request = {
    headers: { ...headers, Authorization: `Bearer ${store.getState().auth.user?.token}` },
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
    return Promise.reject();
  }
  return Promise.resolve();
};

export const ClearCurrentProject = () => async (dispatch: Dispatch<Action>): Promise<void> => {
  dispatch({ type: ActionType.CLEAR_CURRENT_PROJECT });
};

export const bindPlutoUserToProject = (installationId: string, code: string) => async (dispatch: Dispatch<Action>): Promise<void> => {
  const request = {
    headers: { ...headers, Authorization: `Bearer ${store.getState().auth.user?.token}` },
    body: { query: bindUserToProjectMutation(installationId, code) },
  };
  try {
    const response = await API.post(apiName, path, request);
    checkErrors(response, 'bindPlutoUser');
    dispatch({
      type: ActionType.BIND_PROJECT_USER_SUCCESS,
    });
  } catch (error) {
    const errorString = getErrorString(error);
    dispatch({
      type: ActionType.BIND_PROJECT_USER_FAILED,
      payload: errorString,
    });
    return Promise.reject();
  }
  return Promise.resolve();
};
