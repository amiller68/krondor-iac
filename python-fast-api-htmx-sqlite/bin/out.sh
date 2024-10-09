#!/usr/bin/env bash
set -o errexit
set -o nounset

# Set the output directory
MODE=$1

if [ "$MODE" == "dev" ]; then
    OUTPUT_DIR="./out"
fi
if [ "$MODE" == "prod" ]; then
    OUTPUT_DIR="./iac/ansible/service/out"
fi

rm -rf $OUTPUT_DIR
mkdir $OUTPUT_DIR

cp -r bin $OUTPUT_DIR
cp -r alembic $OUTPUT_DIR
rm -r $OUTPUT_DIR/alembic/**/__pycache__
cp -r alembic.ini $OUTPUT_DIR
cp -r app $OUTPUT_DIR
cp -r static $OUTPUT_DIR
cp -r templates $OUTPUT_DIR
cp -r requirements.in $OUTPUT_DIR
cp -r Dockerfile $OUTPUT_DIR
cp -r .env.$MODE $OUTPUT_DIR/.env