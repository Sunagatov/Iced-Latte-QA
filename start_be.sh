#!/usr/bin/env bash

be_hash=$1
if [[ -z "$be_hash" ]]
then
  be_hash=$(git ls-remote https://github.com/Sunagatov/Iced-Latte.git development | head -c7)
else
  be_hash=$(echo "$be_hash" | head -c7)
fi

# TODO: replace development with master when BE team ensures that master is error-prone
export DOCKER_IMAGE_TAG=development-${be_hash}
# remove all QA containers and all volumes
docker-compose -f docker-compose.local.yml down -v
# start QA containers
docker-compose -f docker-compose.local.yml up -d --build