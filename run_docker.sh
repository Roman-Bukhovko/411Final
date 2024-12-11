#!/bin/bash

# Variables
IMAGE_NAME="stock_trader"
CONTAINER_TAG="0.2.0"
HOST_PORT=5000
CONTAINER_PORT=5000
BUILD=true  # Set this to true if you want to build the image

# Check if we need to build the Docker image
if [ "$BUILD" = true ]; then
  echo "Building Docker image..."
  docker build -t ${IMAGE_NAME}:${CONTAINER_TAG} .
else
  echo "Skipping Docker image build..."
fi

# Run the Docker container with the necessary ports and volume mappings
echo "Running Docker container..."
docker run --network host -d \
  --name ${IMAGE_NAME}_container \
  -p ${HOST_PORT}:${CONTAINER_PORT} \
  ${IMAGE_NAME}:${CONTAINER_TAG}

echo "Docker container is running on port ${HOST_PORT}."