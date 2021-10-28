import { IProject, IUser } from '../types/types';

export enum ActionType {
  SIGNIN = 'SIGNIN',
  SIGNOUT = 'SIGNOUT',
  GET_PROJECTS_SUCCESS = 'GET_PROJECTS_SUCCESS',
  PROJECTS_LOADING = 'PROJECTS_LOADING',
  GET_PROJECTS_FAILED = 'GET_PROJECTS_FAILED',
  CREATE_PROJECT_SUCCESS = 'CREATE_PROJECT_SUCCESS',
  CREATE_PROJECT_FAILED = 'CREATE_PROJECT_FAILED',
  GET_CURRENT_PROJECT_SUCCESS = 'GET_CURRENT_PROJECT_SUCCESS',
  GET_CURRENT_PROJECT_FAILED = 'GET_CURRENT_PROJECT_FAILED',
  CLEAR_CURRENT_PROJECT = 'CLEAR_CURRENT_PROJECT',
  BIND_PROJECT_USER_SUCCESS = 'BIND_PROJECT_USER_SUCCESS',
  BIND_PROJECT_USER_FAILED = 'BIND_PROJECT_USER_FAILED',
}

interface actionSignin {
  type: ActionType.SIGNIN;
  payload: IUser;
}

interface actionSignout {
  type: ActionType.SIGNOUT;
}

interface actionGetProjectsSuccess {
  type: ActionType.GET_PROJECTS_SUCCESS;
  payload: IProject[]
}

interface actionProjectsLoading {
  type: ActionType.PROJECTS_LOADING;
}

interface actionGetProjectsFailed {
  type: ActionType.GET_PROJECTS_FAILED;
  payload: string,
}

interface actionCreateProjectSuccess {
  type: ActionType.CREATE_PROJECT_SUCCESS;
}
interface actionCreateProjectFailed {
  type: ActionType.CREATE_PROJECT_FAILED;
  payload: string,
}
interface actionGetCurrentProjectSuccess {
  type: ActionType.GET_CURRENT_PROJECT_SUCCESS;
  payload: IProject,
}
interface actionGetCurrentProjectFailed {
  type: ActionType.GET_CURRENT_PROJECT_FAILED;
  payload: string,
}
interface actionClearCurrentProject {
  type: ActionType.CLEAR_CURRENT_PROJECT
}
interface actionBindProjectUserSuccess {
  type: ActionType.BIND_PROJECT_USER_SUCCESS
}
interface actionBindProjectUserFailed {
  type: ActionType.BIND_PROJECT_USER_FAILED
  payload: string,
}

export type Action = actionSignin | actionSignout | actionGetProjectsSuccess | actionProjectsLoading | actionGetProjectsFailed |
  actionCreateProjectSuccess | actionCreateProjectFailed | actionGetCurrentProjectSuccess | actionGetCurrentProjectFailed |
  actionClearCurrentProject | actionBindProjectUserSuccess | actionBindProjectUserFailed;
