# litestar_project

## Overview

litestar_project is a template project built using the [Litestar](https://www.litestar.dev) framework and [Pydantic](https://pydantic-docs.helpmanual.io). It is designed to kickstart development of scalable and performant web applications.

## Project Structure

The repository is organized as follows:

- **src/litestar_project/**: Contains the main application code.
- **src/scripts/**: Contains utility scripts, including a test runner (invoked as described below).

Other important files include:

- **.gitignore**: Specifies files and directories to ignore in version control.
- **.python-version**: Specifies the required Python version (3.12).
- **pyproject.toml**: Contains project configuration, dependencies, and build settings.
- **uv.lock**: Lock file with exact dependency versions.

## Requirements

- Python 3.12 or higher
- Dependencies managed via Hatchling, as specified in [pyproject.toml](pyproject.toml)
- UV as a package manager, as specified in [pyproject.toml](pyproject.toml)
- PostgreSQL database

## Environment Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory with the following settings:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test
DIRECT_URL=postgresql://postgres:postgres@localhost:5432/test

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### Database Setup

1. Local Development:
   ```bash
   # Start PostgreSQL using Docker
   ./src/scripts/setup-test.sh
   
   # Apply database migrations
   uv run prisma migrate dev
   ```

2. Production:
   - Ensure PostgreSQL is running and accessible
   - Set proper DATABASE_URL and DIRECT_URL in environment
   - Run migrations: `uv run prisma migrate deploy`

### Environment Variables

| Variable      | Description                           | Default               | Required |
|--------------|---------------------------------------|----------------------|----------|
| DATABASE_URL | Primary database connection URL       | -                    | Yes      |
| DIRECT_URL   | Direct database connection (for Prisma) | -                  | Yes      |
| ENV          | Environment name                      | development          | No       |

## Getting Started

### Setup

- Install uv via Homebrew:
  ```bash
  brew install uv
  ```

- Sync dependencies:
  ```bash
  uv sync
  ```

- Set up environment:
  ```bash
  cp .env.example .env  # Copy example env file
  # Edit .env with your settings
  ```

### Run the server
  ```bash
  uv run server
  ```

### Test
  ```bash
  uv test --mypy --ruff --pytest
  ```

## Development

### Database Migrations

1. Create a new migration:
   ```bash
   uv run prisma migrate dev --name <migration_name>
   ```

2. Apply pending migrations:
   ```bash
   uv run prisma migrate deploy
   ```

3. Reset database (development only):
   ```bash
   uv run prisma migrate reset
   ```

### Code Style

The project uses:
- Ruff for linting and formatting
- MyPy for type checking
- Pytest for testing

Run all checks:
```bash
uv test --mypy --ruff --pytest
```

## System Architecture

The system is built using AWS services and Supabase for persistence. Here's the system architecture:

```mermaid
graph LR
    subgraph aws[AWS]
        subgraph dns[Domain Name Service]
            routeer[Route53]
        end
        
        subgraph lb[API Gateway]
            elb[Elastic Load Balancer]
        end
        
        subgraph ecs[Application Server]
            service[ECS Service]
            container[Container]
        end
    end
    
    subgraph ext[External Services]
        supabase[(Supabase DB)]
    end
    
    routeer --> elb
    elb --> service
    service --> container
    container --> supabase
```

### Component Overview

- **Route53**: DNS management and routing
- **Elastic Load Balancer**: API Gateway and load distribution
- **ECS**: Container orchestration and application hosting
- **Supabase**: Database and persistence layer

## Deployment Architecture

The project uses AWS ECS for container orchestration with a GitHub Actions-based CI/CD pipeline. Here's the deployment flow:

```mermaid
architecture-beta
    
    group aws(cloud)[aws]
    group ecs(cloud)[ECS] in aws
    service ecs_service(server)[ECS Service] in ecs
    service ecs_container(server)[ECS Container] in ecs

    group iam(server)[IAM] in aws
    service role(server)[Assume Role] in iam

    group ecr(database)[ECR] in aws
    service registry(database)[Container Registry] in ecr

    group github(cloud)[GitHub]
    service actions(server)[GitHub Actions] in github

    
    actions:R --> L:role
    role:R --> L:registry
    registry:R --> L:ecs_service
    ecs_service:L --> R:ecs_container
```

### CI/CD Process

When a manual release is triggered:

1. GitHub Actions workflow is initiated
2. Workflow assumes an IAM role in AWS
3. Container image is built and pushed to ECR
4. ECS service is updated with the new container image
5. ECS deploys the new container
