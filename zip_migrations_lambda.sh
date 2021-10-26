#!/bin/bash
set -e
FOLDER="zip-migrations-folder"

if [[ -z $S3_BUCKET || -z $S3_ZIP_FILE || -z $S3_PATH ]]; then
  echo '(zip_migrations_lambda.sh) One or more variables are undefined'
  exit 1
fi

rm -rf $FOLDER
mkdir -p $FOLDER/app/utils
cp backend/endpoints/app/models.py $FOLDER/app
cp backend/endpoints/app/utils/response_utils.py $FOLDER/app/utils
cp backend/endpoints/alembic.ini $FOLDER/
cp -r backend/endpoints/migrations $FOLDER/
cp backend/endpoints/requirements_migrations.txt $FOLDER
pip install -r $FOLDER/requirements_migrations.txt -t $FOLDER
cd $FOLDER && zip -q -r ../$S3_ZIP_FILE . && cd ..
ls -l *.zip
aws s3 cp $S3_ZIP_FILE s3://$S3_BUCKET/$S3_PATH/
