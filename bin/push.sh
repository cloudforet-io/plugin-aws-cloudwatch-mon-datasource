#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/aws-cloudwatch:1.0
docker push spaceone/aws-cloudwatch:1.0
