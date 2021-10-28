# GraphQL endpoint(s) and Lambda functions for Pluto

## The Docker images
- Dockerfile
  - Lambda function providing GraphQL endpoints for Pluto application
- Dockerfile_migrations
  - Lambda function providing the database migration support
- Dockerfile_app_webhook
  - Lambda function providing a REST API endpoint for receiving Github Application webhook calls (WIP)


## Testing locally

Start the database and the lambda container

```docker-compose -f docker-compose.lambda.yml up --build```

## JWT Token verification
JWT token verification is implemented as helper module/class in utils/jwt_common.py based on the awslabs example
https://github.com/awslabs/aws-support-tools/tree/master/Cognito/decode-verify-jwt


### Testing with github
You need to run the app_webhook.py _locally_, NOT in the docker container, for local testing. Docker image requires 
lambda requests to be wrapped. Look at test_events directory and `curl` examples below

```
npm install smee-client
<whateverprefix>/node_modules/smee-client/bin/smee.js --url https://smee.io/uWatVYwaiyRN8oF --target http://localhost:8081/pluto-app
```

## Sending direct API calls
If you're running the backend Python code locally you can utilise the Ariadne HTML UI with browser at address
http://localhost:8080 for sending GraphQL queries to the backend. Please see 'Example GraphQL query payloads'

Test payloads against available APIs can be found from test_events/direct_payloads directory

### Test Github App webhook receiving endpoint
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/direct_payloads/app_webhook_install.json" \
"http://localhost:8081/pluto-app"
```

### Test Cognito post confirmation event test endpoint
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/direct_payloads/app_post_confirmation.json" \
"http://localhost:8083/post-confirm"
```

## Invoking lambda functions inside running docker container
You can do lambda invocations by using the curl commands below against running docker containers. If you're in need to
access the APIs running purely on local see 'Sending direct API calls'

Lambda function invocation payloads for testing purposes can be found from test_events/lambda_invocations directory.

### Create database user and database schema
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/create_db.json" \
"http://localhost:9004/2015-03-31/functions/function/invocations"
```

### Drop database schema
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/drop_db.json" \
"http://localhost:9004/2015-03-31/functions/function/invocations"
```

### Drop database user
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/drop_db_user.json" \
"http://localhost:9004/2015-03-31/functions/function/invocations"
```

### Create database user and database
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/create_db.json" \
"http://localhost:9004/2015-03-31/functions/function/invocations"
```

### Invoke db migrations (alembic upgrade head)
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/migrate_db.json" \
"http://localhost:9001/2015-03-31/functions/function/invocations"
```

### Test Cognito post confirmation event test endpoint
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/app_post_confirmation.json" \
"http://localhost:9003/2015-03-31/functions/function/invocations"
```

### Bind pluto user to project user
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/bind_project_user.json" \
"http://localhost:9000/2015-03-31/functions/function/invocations"
```

### Get all projects
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/list_projects.json" \
"http://localhost:9000/2015-03-31/functions/function/invocations"
```

### Call Pluto app (Github) webhook endpoint
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/lambda_invocations/github_app_webhook.json" \
"http://localhost:9002/2015-03-31/functions/function/invocations"
```

## Example GraphQL query payloads

### Get all projects by organisation
```
query { 
  projectsByOrg(organisationUuid: "5ee493f5-f15e-4899-9001-842642ff5a04") 
  { 
    success 
    errors 
    projects 
    { 
      name 
      description 
    }
  }
}
```

### Create a project
```
mutation { 
  createProject(name: "test-project", description: "This is my awesome project") 
  {
    success 
    errors 
    project 
    { 
      name 
      description 
    }
  }
}
```

### Get all projects in the database
```
query { 
  projects
  { 
    success 
    errors 
    projects 
    { 
      name 
      description 
    }
  }
}
```

### Get a specific project in the database
```
query { 
  project(projectUuid: "ac14cdad-593f-4c71-92e5-f97d2929dbf3")
  { 
    success 
    errors 
    project 
    { 
      name 
      description 
    }
  }
}
```

### Update project description
```
mutation { 
  updateDescription(projectUuid: "afdb1ba1-6e9f-40c3-8c34-0777af9153fd", description: "Updated description") 
  {
    success 
    errors 
    project 
    { 
      name 
      description 
    }
  }
}

```
### Delete project
```
mutation { 
  deleteProject(projectUuid: "1b473bb9-8712-4808-b4a8-c1f03d573eae") 
  {
    success 
    errors 
  }
}
```
