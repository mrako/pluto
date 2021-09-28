# Projects endpoint Lambda for Pluto

## Testing locally

Start the database and the lambda container

```docker-compose -f docker-compose.lambda.yml up --build```

Make a request to the function

```curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'```
