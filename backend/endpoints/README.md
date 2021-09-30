# Projects endpoint Lambda for Pluto

## Testing locally

Start the database and the lambda container

```docker-compose -f docker-compose.lambda.yml up --build```

## Sending GraphQL queries

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
