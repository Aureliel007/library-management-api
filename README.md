# Library Management API

This project provides a RESTful API for managing a library. It includes functionality for managing books, readers, and book lending operations. Authentication is handled using JWT tokens.

## Features

- **User Authentication** — secure login with JWT.

- **Book Management** — create, read, update, and delete book records.

- **Reader Management** — manage library users (readers).

- **Book Lending System** — borrow and return books.

- **Auto-generated API Documentation** — available via Swagger UI.

## Requirements

- [Docker](https://www.docker.com/)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure Environment Variables

Create a .env file in the root directory of the project. Use the following template:

```env
POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=<your_database_name>

JWT_SECRET_KEY=<your_secret_key_for_JWT>
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Replace placeholders with your values.

SECRET_KEY is a secret string used to sign JWT tokens. You can generate one with Python:

```Python
import secrets
print(secrets.token_hex(32))
```

### 3. Launch the Project

Run the following command in the project root:

```bash
docker compose up --build
```

This command will start the API service and the PostgreSQL database in Docker containers.

### 4. Access the API Documentation

Once the services are running, you can access the interactive API documentation (Swagger UI) in your browser:

```
http://<your-server-address>:<port>/docs
```

For example, if running locally:

```
http://localhost:8080/docs
```
