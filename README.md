#### Overview
This project sets up a simple web server using Flask that responds to three main endpoints (/home, /heartbeat, /add, /rm). The server is containerized using Docker and managed using Docker Compose to create multiple instances. A load balancer is implemented to distribute the requests across these instances using consistent hashing. Additionally, the system includes monitoring and logging mechanisms to track server health and request distribution.

#### Purpose
The purpose of this project is to demonstrate the implementation of a load balancer that evenly distributes incoming traffic to multiple server instances, ensuring efficient handling of requests and high availability.

#### Components
1. **Web Server**: Handles HTTP requests and provides endpoints for home and heartbeat. Each server instance runs inside a Docker container, making it easy to scale horizontally by adding more instances. The web server also includes basic health checks to ensure each instance is operational.
2. **Consistent Hash Map**: Used for mapping client requests to server instances. The consistent hash map ensures that the addition or removal of servers minimally impacts the mapping of existing requests. This reduces the need for rehashing and helps maintain a stable request distribution across servers.
3. **Load Balancer**: Routes client requests using consistent hashing and manages server replicas. It monitors the health of server instances using heartbeat signals and dynamically adjusts the server pool based on load and server availability. The load balancer can also redistribute requests in case of server failures to ensure continuous service availability.

**System Architecture Diagram**:
```plaintext
+---------------------+
|      Client         |
+---------+-----------+
          |
          v
+---------+-----------+
|    Load Balancer    |
+---------+-----------+
          |
  +-------+-------+
  |       |       |
  v       v       v
+---+   +---+   +---+
| S |   | S |   | S |
| e |   | e |   | e |
| r |   | r |   | r |
| v |   | v |   | v |
| e |   | e |   | e |
| r |   | r |   | r |
| 1 |   | 2 |   | 3 |
+---+   +---+   +---+
```

---

### Assumptions

1. **Network Reliability**: Assumes a reliable network with minimal packet loss. The system is designed to handle transient network issues, but prolonged network failures could affect performance.
2. **Uniform Load Distribution**: Assumes that client requests are uniformly distributed. If the requests are skewed towards specific keys, additional mechanisms might be needed to balance the load more effectively.
3. **Server Homogeneity**

### Prerequisites
1. Docker: latest [version 20.10.23, build 7155243]
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

2.  Docker-compose standalone [version v2.15.1]
   sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose 

**Docker**: To containerize the application.

2. **Python**: For implementing the server, load balancer, and consistent hash map.
3. **Flask**: For handling HTTP requests within the server and load balancer.
4. **Git**: For version control and managing the project repository.


---

### Installation Steps

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/alexwafula/Customizable_Load_Balancerr.git
   cd Customizable_Load_Balancerr
   ```

2. **Build Docker Images**:

   ```sh
   docker-compose build
   ```

3. **Run Docker Containers**:

   ```sh
   docker-compose up
   ```

#### Functional Tests
1. **Test Endpoints**:
   - Use tools like `curl` or Postman to test the following endpoints:
     - `/home`: Returns a unique identifier for the server.
     - `/heartbeat`: Returns the heartbeat status.
     - `/rep`: Checks the status of replicas.
     - `/add`: Adds a new server instance.
     - `/rm`: Removes a server instance.

   Example using `curl`:

   ```sh
   curl http://localhost:5000/home
   curl http://localhost:5000/heartbeat
   curl -X POST http://localhost:5000/add -d 'server_id=new_server'
   curl -X DELETE http://localhost:5000/rm -d 'server_id=existing_server'
   ```

#### Performance Tests
1. **Load Testing**:
   - Use tools like `Apache JMeter` or `Locust` to simulate high traffic and observe the load distribution and fault tolerance.

2. **Experiment Scenarios**:
   - **A-1**: Launch 10000 async requests on 3 server containers and report the request count handled by each server instance.
   - **A-2**: Increment server instances from 2 to 6, launching 10000 requests on each increment, and report the average load.
   - **A-3**: Test all load balancer endpoints and demonstrate quick spawning of new instances upon server failure.
   - **A-4**: Modify hash functions and observe changes from A-1 and A-2.

By following these sections, you can understand the design, implement the distributed queue with sharding, and set up and test the customizable load balancer.


**Task 1: Server Implementation**

**Overview:**
In Task 1, we implemented a simple web server that accepts HTTP requests on port 5000 and provides two endpoints: `/home` and `/heartbeat`. The `/home` endpoint returns a string with a unique identifier to distinguish among replicated server containers. The `/heartbeat` endpoint sends heartbeat responses upon request, allowing the load balancer to identify failures in the set of containers maintained by it.

**Implementation:**
We implemented the server using Python, utilizing the Flask framework for handling HTTP requests. The server runs on port 5000 and provides the required endpoints as specified in the assignment. The server's unique identifier is set as an environment variable while running a container instance from the Docker image of the server.

**Dockerfile:**
We included a Dockerfile to containerize the server as an image, making it deployable for subsequent tasks. The Dockerfile installs necessary dependencies and sets up the environment for running the Flask application.

**Deployment:**
To deploy the server, build the Docker image using the provided Dockerfile and run a container instance from the built image. Ensure that the container is exposed on port 5000 to accept incoming HTTP requests.

**Task 2: Consistent Hashing Implementation**

**Overview:**
In Task 2, we implemented a consistent hash map using Python, which serves as the underlying data structure for the load balancer in Task 3. We utilized an array-based implementation to represent the hash map, with provisions for handling collisions using linear or quadratic probing.

**Implementation:**
We implemented the consistent hash map using Python, utilizing an array data structure to represent the hash map and hash functions provided in the assignment. The implementation ensures that requests are mapped to the appropriate server instances based on the consistent hashing algorithm.

**Task 3: Load Balancer Implementation**

**Overview:**
Task 3 involves building a load balancer container that uses the consistent hashing data structure from Task 2 to manage a set of server replicas. The load balancer is responsible for routing client requests to server replicas in a balanced manner and maintaining the desired number of replicas even in case of failure.

**Implementation:**
We implemented the load balancer container using Python and Flask, leveraging the consistent hashing data structure implemented in Task 2. The load balancer provides HTTP endpoints for modifying configurations, checking the status of managed web server replicas, and routing client requests to server replicas.

**Endpoints:**
- `/rep`: Returns the status of the replicas managed by the load balancer.
- `/add`: Adds new server instances to scale up with increasing client numbers.
- `/rm`: Removes server instances to scale down with decreasing client or system maintenance.
- `/<path>`: Routes client requests to a server replica as scheduled by the consistent hashing algorithm.

**Deployment:**
Deploy the load balancer container using the provided Dockerfile, Docker-compose file, and Makefile. Ensure that the load balancer is exposed on port 5000 to accept incoming HTTP requests.


**Conclusion:**
Overall, the load balancer implementation effectively distributes the load among server containers and demonstrates scalability and fault tolerance. The analysis provides insights into the performance and behavior of the load balancer in various scenarios, contributing to the understanding of distributed systems and load balancing techniques. The other testing images are found in rm_responses.json.

Footer
