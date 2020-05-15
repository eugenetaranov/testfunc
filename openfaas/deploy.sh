#!/bin/bash
set -e
set -x

export DOCKER_REPO=1234567890.dkr.ecr.us-east-1.amazonaws.com/
export OPENFAAS_URL=http://openfaas.testdomain.com


for f in public-input kafka-consumer hasura-auth
do
    cd functions/${f}
    faas-cli up -f ${f}.yml
    cd $OLDPWD
done
