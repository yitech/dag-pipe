
# Running Redis in Docker

This guide will show you how to host a Redis instance in a Docker container.

## Prerequisites

Make sure you have Docker installed on your machine. If not, you can download it from the [official Docker website](https://www.docker.com/get-started).

## Steps

### 1. Pull the Redis image from Docker Hub

You can pull the latest Redis image by running the following command in your terminal:

```bash
docker pull redis
```

### 2. Run Redis in a Docker container

After pulling the image, you can start a Redis instance with this command:

```bash
docker run --name unwear-redis -d -p 6379:6379 redis
```

This command does the following:

- `docker run` starts a new Docker container.
- `--name unwear-redis` names the container "some-redis". You can choose a different name if you prefer.
- `-d` runs the container in the background (i.e., "detached" mode).
- `-p` expose Redis to the host machine or other containers
- `redis` specifies the image to use for the container.

This command maps port 6379 in the container (the default Redis port) to port 6379 on your host machine. You can then connect to Redis using this port.


