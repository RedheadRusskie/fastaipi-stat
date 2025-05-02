# Fastapi-Stat

<p align="center">
  <img src="https://github.com/RedheadRusskie/fastaipi-stat/blob/develop/assets/stat-con.svg" alt="Logo" width="200" />
</p>

<p align="center">
  A lightweight BE application built with Python and FastAPI, PostgreSQL for data persistence, and Docker for seamless deployment.
</p>

## Tech Stack

- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Environment Management**: Pydantic
- **Containerisation**: Docker, Docker Compose

## Table of Contents

- [Installation](#installation)
- [Environment](#environment)
- [Usage](#usage)

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/RedheadRusskie/fastaipi-stat.git
```

## Environment

Create a `.env` file in the root directory. You can use this template:

```env
# PostgreSQL environment variables
POSTGRES_DB=db-name
OSTGRES_USER=db-user
POSTGRES_PASSWORD=db-password
POSTGRES_DB_PORT=db-port

# FastAPI app configuration
APP_HOST_PORT=fastapi-port

# Auth
AUTH_SECRET=your-secret
```

If using Docker, you can also define this in the `docker-compose.yml` file under the `environment` section.

## Usage

Build the containers with:

```bash
docker compose -f docker-compose.yaml build
```

And spin up with with:

```bash
docker compose -f docker-compose.yaml up -d
```

The FastAPI server will be available at: [http://localhost:8000](http://localhost:8000)  
Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
