# Pipeline

This application uses RabbitMQ as a messaging broker. This README provides instructions on how to set up RabbitMQ as a prerequisite for running the application.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.

## Setting up RabbitMQ

Follow the steps below to set up RabbitMQ using Docker:

1. **Pull the RabbitMQ Docker image:** Open a terminal or command prompt and run the following command to pull the official RabbitMQ image from Docker Hub:

   ```
   docker pull rabbitmq:3-management
   ```

   This command pulls the RabbitMQ image with the management plugin enabled. The management plugin provides a web-based user interface to manage and monitor RabbitMQ.

2. **Run the RabbitMQ container:** Run the following command to create and start a RabbitMQ container:

   ```
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

   This command runs the RabbitMQ container in detached mode (`-d`) and maps the container's ports 5672 (RabbitMQ) and 15672 (management plugin) to your local machine's ports. The `--name` flag assigns a name to the container for easier reference.

3. **Access RabbitMQ Management Plugin (optional):** Now that the RabbitMQ container is running, you can access the web-based management plugin by visiting [http://localhost:15672/](http://localhost:15672/) in your browser. The default username and password are both "guest".

You have now set up RabbitMQ locally using Docker. You can proceed to build and run the application.

## Stopping and Removing RabbitMQ Container

When you're done using the application, you can stop and remove the RabbitMQ container by running the following commands:

```
docker stop rabbitmq
docker rm rabbitmq
```

## Additional Resources

- [RabbitMQ Official Website](https://www.rabbitmq.com/)
- [RabbitMQ Docker Hub Repository](https://hub.docker.com/_/rabbitmq)
- [Docker Official Website](https://www.docker.com/)