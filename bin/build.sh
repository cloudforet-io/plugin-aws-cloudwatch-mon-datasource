#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/aws-cloudwatch .
docker tag pyengine/aws-cloudwatch pyengine/aws-cloudwatch:1.0
docker tag pyengine/aws-cloudwatch spaceone/aws-cloudwatch:1.0
