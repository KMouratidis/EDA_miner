#!/bin/bash

# source: https://blog.jevsejev.io/2016/06/09/docker-image-tests/
dockerImage=$1
echo "Testing $dockerImage..."

# Bail the script as soon as something is wrong. No need to execute further
set -eo pipefail

# Enable debug mode
[ "$DEBUG" ] && set -x

# cd to directory of script
cd "$(dirname "$0")"

# test if docker image exists
if ! sudo docker inspect "$dockerImage" &> /dev/null; then
    echo $'\timage does not exist!'
    false
fi

# Create an instance of the container-under-test
cid="$(docker run -d "$dockerImage")"
# Remove container afterwards
trap "docker rm -vf $cid > /dev/null" EXIT
docker exec -it $cid [ -S $socketFile ] || (echo "Socket $socketFile is not found" && exit 1)

echo "Testing successful."
