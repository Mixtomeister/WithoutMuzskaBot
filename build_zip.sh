#! /bin/bash

pip install \
    --target ./package \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: --upgrade \
    -r requirements.txt

cd package
zip -r ../lambda_deploy_package.zip .

cd ..
zip -g lambda_deploy_package.zip bot.py
rm -rf ./package
