# Litestar Project Template

A production-ready template for building scalable web applications using [Litestar](https://www.litestar.dev) and [Pydantic](https://pydantic-docs.helpmanual.io).

## Quick Start

1. Install UV:
   ```bash
   brew install uv
   ```

2. Set up environment:
   ```bash
   cp .env.example .env
   uv sync
   ```

3. Start database and run migrations:
   ```bash
   ./src/scripts/setup-test.sh
   uv run prisma migrate dev
   ```

4. Run the server:
   ```bash
   uv run server
   ```

## Development Guide

### Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- UV package manager

### Environment Setup

Create a `.env` file with the following configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test
DIRECT_URL=postgresql://postgres:postgres@localhost:5432/test

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

#### Environment Variables

| Variable      | Description                           | Required | Default     |
|--------------|---------------------------------------|----------|-------------|
| DATABASE_URL | Primary database connection URL       | Yes      | -           |
| DIRECT_URL   | Direct database connection (Prisma)   | Yes      | -           |
| HOST         | Server host address                   | No       | 0.0.0.0     |
| PORT         | Server port                           | No       | 8000        |

### Database Management

#### Local Development
```bash
# Start PostgreSQL
./src/scripts/setup-test.sh

# Create migration
uv run prisma migrate dev --name <migration_name>

# Apply migrations
uv run prisma migrate deploy

# Reset database (dev only)
uv run prisma migrate reset
```

#### Production Setup
- Ensure PostgreSQL is accessible
- Configure DATABASE_URL and DIRECT_URL
- Run `uv run prisma migrate deploy`

### Testing and Quality

Run all checks:
```bash
uv test --mypy --ruff --pytest
```

The project uses:
- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Pytest**: Testing

## Project Structure

```
.
├── src/
│   ├── litestar_project/  # Main application code
│   └── scripts/           # Utility scripts
├── tests/                 # Test suite
├── .env.example          # Environment template
├── .python-version       # Python version spec
├── pyproject.toml        # Project configuration
└── uv.lock              # Dependency lock file
```

## Deployment

### Infrastructure Overview

The application is deployed on AWS using:
- **Route53**: DNS management
- **API Gateway/ELB**: Load balancing
- **ECS**: Container orchestration
- **ECR**: Container registry
- **Supabase**: Database service

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

### CI/CD Pipeline

Automated deployment using GitHub Actions:

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

#### Deployment Process

1. Trigger deployment via GitHub Actions
2. AWS IAM role assumption
3. Build and push container to ECR
4. Update ECS service
5. Deploy new container version
