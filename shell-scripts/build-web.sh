#!/bin/bash
set -e

# Build and push the Django web Docker image to GitLab registry.
# Usage: ./build-web.sh [TAG]
# TAG defaults to "latest" if not provided.

TAG="${1:-latest}"
REGISTRY="registry.gitlab.com"
WEB_IMAGE="${REGISTRY}/pyung/ng-pycon/ng-pycon-web:${TAG}"

echo "Starting web Docker build and push..."
echo "Tag: ${TAG}"
echo "Building image: ${WEB_IMAGE}"

docker build -t "${WEB_IMAGE}" --no-cache --progress=plain .

echo "Image built successfully"
echo "Pushing image to registry..."

docker push "${WEB_IMAGE}"

echo "Image pushed successfully: ${WEB_IMAGE}"
