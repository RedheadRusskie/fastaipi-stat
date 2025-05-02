# Fastapi-Stat

<p align="center">
  <img src="" alt="Logo" width="200" />
</p>

<p align="center">
  A lightweight, full-stack to-do list application built with Python and FastAPI on the backend, PostgreSQL for data persistence, and Docker for seamless deployment.
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
- [Building](#building)
- [Testing](#testing)

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/RedheadRusskie/fastaipi-stat.git
```

## Environment

Create a `.env` file in the root directory. You can use this template:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/tododb
```

If using Docker, you can also define this in the `docker-compose.yml` file under the `environment` section.

## Usage (Docker Compose Recommended)

Spin up the stack with:

```bash
docker compose -f docker-compose.yml up -d
```

The FastAPI server will be available at: [http://localhost:8000](http://localhost:8000)  
Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running the project

Rebuild the Docker containers if needed:

```bash
docker compose -f docker-compose.yml build
```

And running with:

```bash
docker compose -f docker-compose.yml up -d
```
