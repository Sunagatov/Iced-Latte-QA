#!/usr/bin/env bash

be_hash=$1
if [[ -z "$be_hash" ]]
then
  github_tag=development-$(git ls-remote https://github.com/Sunagatov/Iced-Latte.git development | head -c7)
  dockerhub_tag=$(curl -s \
    'https://hub.docker.com/v2/repositories/zufarexplainedit/iced-latte-backend/tags?page_size=1' | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['results'][0]['name'])")
  if [[ "$github_tag" != "$dockerhub_tag" ]]; then
    echo 'WARN: difference between GitHub and DockerHub commits. Most likely BE deploy job failed.'
  fi
  echo "Using the latest DockerHub tag $dockerhub_tag"
  tag=$dockerhub_tag
else
  echo "Using specified DockerHub tag $be_hash"
  tag=$be_hash
fi

# TODO: replace development with master when BE team ensures that master is error-prone
export DOCKER_IMAGE_TAG=${tag}
# remove all QA containers and all volumes
docker-compose -f docker-compose.local.yml down -v
# start QA containers
docker-compose -f docker-compose.local.yml up -d --build