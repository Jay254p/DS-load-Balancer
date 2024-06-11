# DS-load-Balancer
### Setting Up and Implementing Task 1 Using WSL

Task 1 involves setting up a simple web server that can respond to two endpoints (`/home` and `/heartbeat`). This server needs to be containerized using Docker. Here are the steps to accomplish this using WSL (Windows Subsystem for Linux).

#### Prerequisites

1.  **WSL and Ubuntu Installation**:

    -   Ensure that you have WSL installed on your Windows machine.
    -   Install Ubuntu from the Microsoft Store.
2.  **Install Docker on WSL**:

    -   Follow the steps provided in the Appendix A of the assignment to install Docker and Docker Compose on your WSL environment.

#### Step-by-Step Implementation of Task 1

1.  **Set Up Your Project Directory**:

    -   Create a new directory for your project and navigate into it.

        bash

        Copy code

        `mkdir load_balancer_project
        cd load_balancer_project`

2.  **Create the Web Server Code**:

    -   Create a file named `server.py` with the following content:

        python

        Copy code

        `from flask import Flask, jsonify
        import os

        app = Flask(__name__)

        # Endpoint /home
        @app.route('/home', methods=['GET'])
        def home():
            server_id = os.getenv('SERVER_ID', 'unknown')
            return jsonify({
                "message": f"Hello from Server: {server_id}",
                "status": "successful"
            }), 200

        # Endpoint /heartbeat
        @app.route('/heartbeat', methods=['GET'])
        def heartbeat():
            return "", 200

        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5000)`

3.  **Create a Dockerfile**:

    -   Create a file named `Dockerfile` with the following content to containerize your server.

        Dockerfile

        Copy code

        `# Use an official Python runtime as a parent image
        FROM python:3.8-slim

        # Set the working directory
        WORKDIR /app

        # Copy the current directory contents into the container at /app
        COPY . /app

        # Install any needed packages specified in requirements.txt
        RUN pip install flask

        # Make port 5000 available to the world outside this container
        EXPOSE 5000

        # Define environment variable
        ENV NAME World

        # Run app.py when the container launches
        CMD ["python", "server.py"]`

4.  **Create a Docker Compose File**:

    -   Create a file named `docker-compose.yml` with the following content to manage multiple instances of your server.

        yaml

        Copy code

        `version: '3'
        services:
          server1:
            build: .
            container_name: server1
            environment:
              - SERVER_ID=1
            ports:
              - "5001:5000"
          server2:
            build: .
            container_name: server2
            environment:
              - SERVER_ID=2
            ports:
              - "5002:5000"
          server3:
            build: .
            container_name: server3
            environment:
              - SERVER_ID=3
            ports:
              - "5003:5000"`

5.  **Build and Run the Docker Containers**:

    -   Execute the following commands to build the Docker images and run the containers.

        bash

        Copy code

        `sudo docker-compose build
        sudo docker-compose up`

6.  **Testing the Endpoints**:

    -   You can now test the endpoints using curl or any HTTP client like Postman.

        bash

        Copy code

        `curl http://localhost:5001/home
        curl http://localhost:5002/home
        curl http://localhost:5003/home
        curl http://localhost:5001/heartbeat
        curl http://localhost:5002/heartbeat
        curl http://localhost:5003/heartbeat`

        Each `/home` endpoint should return a message indicating the server ID. Each `/heartbeat` endpoint should return an empty response with a 200 status code.