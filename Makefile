.PHONY: build up down

# Build the Docker images
build:
	docker-compose build

# Start the Docker containers
up:
	docker-compose up

# Stop and remove the Docker containers
down:
	docker-compose down

