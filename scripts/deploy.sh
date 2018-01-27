#!/usr/bin/env bash
#   Use this script to deploy the container to ECR and update elastic beanstalk

docker --version  
pip install --user awscli 
export PATH=$PATH:$HOME/.local/bin 
eval $(aws ecr get-login --no-include-email --region us-west-1) 
docker build -f Dockerfile.aws -t feature-webapp .
docker tag feature-webapp:latest 023247576146.dkr.ecr.us-west-1.amazonaws.com/feature-webapp:latest
docker push 023247576146.dkr.ecr.us-west-1.amazonaws.com/feature-webapp:latest
aws --region us-west-1 elasticbeanstalk update-environment --environment-name features-webapp --version-label 1.1