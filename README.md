# DS-load-Balancer
# Prerequisites
### 1. Docker: latest [version 20.10.23, build 7155243]

    sudo apt-get update

    sudo apt-get install \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io

### 2. Docker-compose standalone [version v2.15.1]
    sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    
    sudo chmod +x /usr/local/bin/docker-compose
    
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

    
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

7.  **Create a Makefile**:

    -   Create a file named `Makefile` to automate the build and run process.

        makefile

        Copy code

        `build:
        	docker-compose build

        up:
        	docker-compose up

        down:
        	docker-compose down`

By following these steps, you should be able to set up and run a simple web server that responds to the specified endpoints and is containerized using Docker, all within a WSL environment.

4o
