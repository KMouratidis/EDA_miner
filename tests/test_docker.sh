#!/bin/bash

# source: https://blog.jevsejev.io/2016/06/09/docker-image-tests/
dockerImageName=$1
dockerImagePath=$2
echo "Testing $dockerImageName..."

# Bail the script as soon as something is wrong. No need to execute further
set -eo pipefail

# Enable debug mode
[ "$DEBUG" ] && set -x

# build the image anew
sudo docker build --rm -t $dockerImageName $dockerImagePath

# Run the container and bootup the server
sudo docker run --rm $dockerImageName sleep 5

echo "Testing successful."
