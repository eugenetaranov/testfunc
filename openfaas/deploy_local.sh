#!/bin/bash
set -e
set -x

export DOCKER_REPO=
export OPENFAAS_URL=$(minikube service -n openfaas gateway-external --url)

eval $(minikube docker-env)

for f in public-input kafka-consumer hasura-auth
do
    cd functions/${f}
    faas-cli build -f ${f}.yml
    faas-cli deploy -f ${f}.yml
    cd $OLDPWD
done
