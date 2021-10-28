import { TypedUseSelectorHook, useSelector } from 'react-redux';
import { useLocation } from 'react-router-dom';
import { RootState } from 'types/types';

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

export function useQuery():URLSearchParams {
  return new URLSearchParams(useLocation().search);
}
