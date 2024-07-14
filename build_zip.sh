#! /bin/bash

pip install --target ./package -r requirements.txt

cd package
zip -r ../lambda_deploy_package.zip .

cd ..
zip -g lambda_deploy_package.zip ./*.py
rm -rf ./package
