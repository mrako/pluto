#!/bin/bash
set -e

if [[ -z $FUNCTION_NAME || -z $ALIAS  ]]; then
  echo 'One or more variables are undefined'
  exit 1
fi

echo "About to invoke lambda: $FUNCTION_NAME alias: $ALIAS"

for i in $(seq 3)
do
    invoke=`aws lambda invoke --function-name $FUNCTION_NAME --qualifier $ALIAS output.txt`
    RESULT=$?

    if [ $RESULT -eq 0 ]; then
        echo "aws lambda invoke status: OK"
        INVOKE_RESULT_SUCCESS=`cat output.txt |jq -r .body | jq .success`
        INVOKE_RESULT_MESSAGE=`cat output.txt |jq -r .body | jq -r .message`
        if [ $INVOKE_RESULT_SUCCESS = "true" ]; then
            echo "aws lambda invoke result status: $INVOKE_RESULT_SUCCESS"
            echo "aws lambda invoke result message: $INVOKE_RESULT_MESSAGE"
            break 1
        fi
    else
        echo "aws lambda update-function-code status: Failed"
        exit 1
    fi
done
