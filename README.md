# DS-load-Balancer

## Overview

This project sets up a simple web server using Flask that responds to three main endpoints (`/home`, `/heartbeat`, `/add`, `/rm`). The server is containerized using Docker and managed using Docker Compose to create multiple instances. A load balancer is implemented to distribute the requests across these instances using consistent hashing.

## Purpose

The purpose of this project is to demonstrate the implementation of a load balancer that evenly distributes incoming traffic to multiple server instances, ensuring efficient handling of requests and high availability.

## Prerequisites

Ensure you have the following installed on your system:

- WSL 2 with Ubuntu 22.04.3
- Docker
- Docker Compose

## Installation Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd DS-load-Balancer