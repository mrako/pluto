import { IProject } from 'types/types';
import { ActionType, Action } from '../actionTypes';

interface IProjectState {
  projects: IProject[],
  currentProject: IProject | null,
  loading: boolean,
  error: string | null,
}

const initState: IProjectState = {
  projects: [],
  currentProject: null,
  loading: false,
  error: null,
};

export default function project(state:IProjectState = initState, action:Action):IProjectState {
  switch (action.type) {
    case ActionType.GET_PROJECTS_SUCCESS: {
      return {
        ...state,
        projects: action.payload,
        loading: false,
        error: null,
      };
    }
    case ActionType.PROJECTS_LOADING: {
      return {
        ...state,
        loading: true,
        error: null,
      };
    }
    case ActionType.CREATE_PROJECT_SUCCESS: {
      return {
        ...state,
        loading: false,
        error: null,
      };
    }
    case ActionType.GET_CURRENT_PROJECT_SUCCESS: {
      return {
        ...state,
        currentProject: action.payload,
        loading: false,
        error: null,
      };
    }
    case ActionType.GET_PROJECTS_FAILED:
    case ActionType.CREATE_PROJECT_FAILED:
    case ActionType.GET_CURRENT_PROJECT_FAILED:
    case ActionType.BIND_PROJECT_USER_FAILED: {
      return {
        ...state,
        projects: [],
        currentProject: null,
        loading: false,
        error: action.payload,
      };
    }
    case ActionType.CLEAR_CURRENT_PROJECT: {
      return {
        ...state,
        currentProject: null,
      };
    }
    case ActionType.SIGNOUT: {
      return { ...initState };
    }
    default: {
      return state;
    }
  }
}
