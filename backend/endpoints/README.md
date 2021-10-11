# GraphQL endpoint(s) and Lambda functions for Pluto

## Testing locally

Start the database and the lambda container

```docker-compose -f docker-compose.lambda.yml up --build```

## Sending GraphQL queries

You can either use the lambda invocation below using the curl commands or if you're running the backend Python code
locally utilise the Ariadne HTML UI with browser at address http://localhost:8080 

### Get all projects
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/list_projects.json" \
"http://localhost:9000/2015-03-31/functions/function/invocations"
```

### Invoke db migrations (alembic upgrade head)
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/migrate_db.json" \
"http://localhost:9001/2015-03-31/functions/function/invocations"
```

### Call Pluto app (Github) webhook endpoint
```
curl -X POST \
-H "Content-Type: application/json" \
-d "@./test_events/github_app_webhook.json" \
"http://localhost:9002/2015-03-31/functions/function/invocations"
```

## Some example GraphQL query payloads

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
### Delete project description
```
mutation { 
  deleteProject(projectUuid: "1b473bb9-8712-4808-b4a8-c1f03d573eae") 
  {
    success 
    errors 
  }
}
```
