#!/bin/bash
set -e

if [[ -z $ECR_URL || -z $FUNCTION_NAME || -z $ALIAS || -z $DESCRIPTION || -z $ECR_REPO || -z $ECR_IMAGE ]]; then
  echo 'One or more variables are undefined'
  exit 1
fi

echo "About to deploy image: $ECR_IMAGE to lambda: $FUNCTION_NAME and set alais: $ALIAS"

update=`aws lambda update-function-code --function-name $FUNCTION_NAME --image-uri $ECR_URL/$ECR_REPO:$ECR_IMAGE --no-publish`
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "aws lambda update-function-code status: Executed"

    for i in $(seq 20)
    do
      sleep 5
      result=`aws lambda list-versions-by-function --function-name $FUNCTION_NAME | jq '.Versions[] | select(.Version== "$LATEST")' | jq -r .LastUpdateStatus`
      if [ "$result" = "InProgress" ]; then
        echo "aws lambda update-function-code status: InProgress"
      else
        break 1
      fi
    done
    RevisionId=`aws lambda list-versions-by-function --function-name $FUNCTION_NAME | jq '.Versions[] | select(.Version== "$LATEST")' | jq -r .RevisionId`
    echo "Publishing RevisionId: $RevisionId"

    version=`aws lambda publish-version --function-name $FUNCTION_NAME --description $ECR_IMAGE --revision-id $RevisionId | jq -r .Version`
    echo "Published RevisionId: $RevisionId -> version: $version"

    echo "Updating lambda alias development -> version $version ($ECR_IMAGE)"
    result=`aws lambda update-alias --function-name $FUNCTION_NAME --name $ALIAS --function-version $version`
else
    echo "aws lambda update-function-code status: Failed"
    exit 1
fi
