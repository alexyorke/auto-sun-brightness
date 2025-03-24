# CI/CD Pipeline for Auto-Sun-Brightness

This project uses GitHub Actions for Continuous Integration and Continuous Deployment. The following workflows are set up:

## Continuous Integration (CI)

The CI pipeline runs on every push to main, pull request to main, and weekly. It performs the following tasks:

- Runs tests on multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Lints the code using flake8
- Verifies the application runs with sample parameters

### Workflow File

`.github/workflows/ci.yml`

## Continuous Deployment (CD)

The CD pipeline runs when a new release is created. It performs the following tasks:

- Builds a Python package
- Publishes the package to PyPI

### Workflow File

`.github/workflows/cd.yml`

## Docker Build and Push

The Docker workflow runs when a new release is created or manually triggered. It performs the following tasks:

- Builds a Docker image for the application
- Pushes the image to Docker Hub

### Workflow File

`.github/workflows/docker.yml`

## Setting Up Required Secrets

For the pipelines to work properly, you need to set up the following secrets in your GitHub repository:

1. For PyPI deployment:

   - `PYPI_API_TOKEN`: Your PyPI API token

2. For Docker Hub deployment:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

### Setting Up Secrets in GitHub

1. Go to your repository on GitHub
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add each secret with its appropriate name and value

## Running the Workflows Manually

1. Go to the "Actions" tab in your GitHub repository
2. Select the workflow you want to run
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## Using the Docker Image

Once published, the Docker image can be used as follows:

```bash
docker run --rm username/auto-sun-brightness:latest --lat 40.7128 --long -74.0060 --max 10 --min 0
```

Replace `username` with your Docker Hub username.

## Creating a New Release

To trigger the deployment pipelines:

1. Go to the "Releases" section in your GitHub repository
2. Click "Create a new release"
3. Tag the release (e.g., v1.0.0)
4. Add a title and description
5. Click "Publish release"

This will automatically trigger both the CD pipeline to publish to PyPI and the Docker workflow to build and push a container.
