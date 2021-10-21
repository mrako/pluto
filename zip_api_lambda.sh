#!/bin/bash
set -e
FOLDER="zip-api-folder"

if [[ -z $S3_BUCKET || -z $S3_ZIP_FILE || -z $S3_PATH ]]; then
  echo '(zip-api-folder.sh) One or more variables are undefined'
  exit 1
fi

rm -rf $FOLDER
mkdir -p $FOLDER
cp -r backend/endpoints/app/* $FOLDER
cp backend/endpoints/requirements.txt $FOLDER
pip install -r $FOLDER/requirements.txt -t $FOLDER
cd $FOLDER && zip -q -r ../$S3_ZIP_FILE . && cd ..
ls -l *.zip
aws s3 cp $S3_ZIP_FILE s3://$S3_BUCKET/$S3_PATH/
