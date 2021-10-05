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