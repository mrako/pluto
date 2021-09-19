export interface IApi {
  get: VoidFunction;
}

export default class Api {
  dispatch: any;

  constructor() {
    this.dispatch = null;
  }

  get(): void {
    console.log(this.dispatch);
  }
}
