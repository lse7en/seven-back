
# Brite Test Project

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Design](#design)
- [GCP Deployment](#gcp-deployment)
- [Local Development and Testing](#local-development-and-testing)
## Overview

This project implements a backend system that interacts with the OMDB API to fetch movie data, save it to a database, and provide an API for accessing and manipulating this data. The project is designed with scalability and security in mind, and it's ready for deployment on Google Cloud Platform (GCP).

## Features

- **Data Fetching**: Automated script to fetch 100 movies from OMDB API and save them to the database.
- **API Endpoints**:
  - List movies with pagination and optional record count per response.
  - Fetch a single movie by title.
  - Add a new movie by title (details fetched from OMDB API).
  - Remove a movie by ID with authorized access.
- **Security**: Protected endpoint to ensure only authorized users can remove movies.
- **Unit Testing**: Comprehensive tests covering all functionalities.
- **Deployment**: Configuration ready for deployment on GCP with Terraform.

## Project Structure

- **`src/`**: Core application code, including API endpoints, services, models, and utilities.
- **`tests/`**: Unit and integration tests.
- **`terraform/`**: Terraform configuration files for GCP deployment.
- **`migrations/`**: Alembic migrations for database schema.
- **`static/`**: Static files, including pre-defined data.
- **`emulators/`**: Utilities for local development.


## Design

The system is architecturally divided into two main services to enhance scalability and maintain a clear separation of concerns:

- **API Service (`src/app_api.py`)**: Acts as the primary interface for user interactions. It handles requests to list movies, fetch a single movie by title, add new movies, and remove movies from the database. When a request to add a new movie is received, the API service first checks if the movie data has already been fetched from the OMDB API. If the movie is not present in the database, it publishes a message to the `fetch` topic on Google Pub/Sub, signaling that the movie data needs to be fetched.

- **Worker Service (`src/app_worker.py`)**: Operates asynchronously to handle background tasks. Upon receiving a message from the `fetch` topic on Google Pub/Sub, the worker service fetches the movie data from the OMDB API and updates the database accordingly. This decoupling allows the API service to remain responsive to user requests while the worker service handles the data fetching and processing tasks in the background.

This design ensures efficient handling of user requests and data processing tasks, enabling the system to scale as needed while maintaining high performance and reliability.


## GCP Deployment

This project is designed for full deployment on Google Cloud Platform (GCP), using a suite of services for optimal performance, scalability, and reliability. Below is an overview of the GCP services used in the project:

- **[Load Balancer](https://cloud.google.com/load-balancing?hl=en)**: Distributes incoming application traffic across Cloud Run services.

- **[Cloud Run](https://cloud.google.com/run)**: Cloud Run is used to host the API and Worker services, allowing them to scale based on demand without manual intervention.

- **[Pub/Sub](https://cloud.google.com/pubsub)**: communication between the API service and the Worker service for movie data fetching tasks.

- **[Cloud SQL](https://cloud.google.com/sql/?hl=en)**: A fully managed relational database service using PostgreSQL. The project uses Cloud SQL to store and manage movie data persistently.


### Prerequisites

Before deploying the project on Google Cloud Platform (GCP), ensure you have the following prerequisites ready:

- **Google Cloud Project**: You can either create a new GCP project specifically for this deployment or use an existing one. If you choose to use an existing project, be aware of potential Terraform exceptions due to pre-existing configurations.

- **Google Cloud SDK (gcloud)**: Install the GCP command-line interface (CLI) tool and authenticate it with your chosen GCP project.

- **Terraform**: Install the latest version of Terraform.

### Deployment

Deploy the application by setting up Terraform variables, initializing Terraform, creating a repository in Google Artifact Registry, and pushing Docker images.

1. **Configure Variables**

   Set the `gcp_project_id` correctly in your Terraform variables.

   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Initialize Terraform**

   ```bash
   terraform init
   ```

3. **Create Repository**

   Create a Google Artifact Registry repository for your Docker images.

   ```bash
   terraform apply --target=google_artifact_registry_repository.repository
   ```

   Copy the provided repository tag for later use.

   ```bash
   export OMDB_PROJECT_TAG='your_repository_tag'
   ```

4. **Push Images**

   Authenticate with the Artifact Registry and push your Docker image. you should be in the root folder of the project.

   ```bash
   gcloud auth configure-docker europe-west1-docker.pkg.dev
   docker build . -f Dockerfile --target production --tag $OMDB_PROJECT_TAG
   docker push $OMDB_PROJECT_TAG
   ```
   you may have to use docker buildx if you are not on linux.
   ```bash
   docker buildx build  . -f Dockerfile --tag $OMDB_PROJECT_TAG   --platform linux/amd64 --target production
   ```
5. **Apply infrastructure**

   ```bash
   terraform apply
   ```
   The output will display the URL where your application is accessible, for example: http://8.8.8.8. Append `/docs` to this URL to view the documentation. Please note, it might take a few minutes for the application to initialize and become fully operational.

6. **Destroy**
   Run to destroy the infrastructure.
   ```bash
   terraform destry
   ```


### Local Development and Testing

To set up your local development environment, ensure you have Docker Compose, Python, and Poetry installed.

#### 1. Set Up

Initialize your development environment using the provided Make command. This will prepare the necessary configurations and dependencies.

```bash
make setup-dev
```

After running the setup, you might want to review the `.env` file for any necessary adjustments, such as updating the OMDB API key if the provided one has expired.

#### 2. Build

Compile the application components into a Docker image.

```bash
make build
```

#### 3. Run

```bash
make run
```
Launch the application locally. Once running, you can access the Swagger documentation at [http://localhost:8080/docs](http://localhost:8080/docs).

#### 4. Tests

Execute the following commands to run different sets of tests:

```bash
make test-units # for unit tests
make test-integration # for integration tests
make test-all # to run all tests
make coverage # to check test coverage
```

For a comprehensive list of available commands, execute:

```bash
make help
```
