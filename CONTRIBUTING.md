# How to start

## Frontend

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\

## Backend

### Python development requirements

You will need to have pipenv installed with your Python as a GLOBAL package
pipenv needs to be in a PATH of you command line console.

```pip3 install pipenv```

So in the command line console initialisation file you need to have something like this:
```export PATH=/what/ever/path/you/may/have/in/your/env/Library/Python/3.9/bin:$PATH```


You need to be able to create virtual environments and the virtual environment directory must be located at the root of
the pluto repository directory.

```python3 -m venv venv```

More importantly the virtual environment directory name _must be_ venv

# Conventions

## Branches
Branches should be named as `<feature/task/bugfix>/<issue number>-description-here`
For example `feature/20-add-authentication`

## Pull requests
If a pull request should close/fix/resolve an issue the description should have a line f.ex closes #2 
This will close issue number 2 when the PR is merged. More info on https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue 
