#!/bin/bash

# Set image name and tag
IMAGE_NAME="financial-tracker"
IMAGE_TAG="latest"

# Define the container name
CONTAINER_NAME="financial-tracker-container"

# Build the Docker image
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Print a message indicating the build status
if [ $? -eq 0 ]; then
  echo "Docker image $IMAGE_NAME:$IMAGE_TAG built successfully."
else
  echo "Failed to build Docker image $IMAGE_NAME:$IMAGE_TAG."
  exit 1
fi

# Run the Docker container
echo "Running the Docker container..."

# Remove the old docker container
docker stop financial-tracker-container
docker rm financial-tracker-container

docker run -d --name $CONTAINER_NAME $IMAGE_NAME:$IMAGE_TAG

# Check if the container started successfully
if [ $? -ne 0 ]; then
  echo "Failed to run the Docker container."
  exit 1
fi

echo "Docker container is running successfully."
