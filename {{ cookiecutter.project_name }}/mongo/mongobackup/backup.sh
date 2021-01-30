#!/bin/bash

set -eo pipefail

DATE=$(date +%Y%m%d_%H%M%S)
FILE="$TARGET_FOLDER/backup-$DATE.gz"

echo "backing up"
echo $MONGO_INITDB_ROOT_USERNAME
echo $(env | grep -i mongo)

echo "Job started: $(date)"

mkdir -p "$TARGET_FOLDER"
mongodump --host="{{cookiecutter.project_name}}_mongo_docker" --archive="$FILE" --gzip --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --db $MONGO_INITDB_DATABASE
# RESTORE OPERATION:
# mongo $MONGO_INITDB_DATABASE --host="mongo_container" --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --eval "db.dropDatabase()"
# mongorestore --archive=/backup/backup-20201017_215601.tar --host="mongo_container" --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD
echo "Mongo dump saved to $FILE"

echo "Job finished: $(date)"
