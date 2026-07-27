# Docker and Docker Compose Guide

This guide explains the `Dockerfile` and `docker-compose.yml` files used in your project. It is designed for beginners and includes best practices, important commands, and a detailed explanation of each line.

---

## What is Docker?
Docker is a platform that allows you to package applications and their dependencies into a container. Containers are lightweight, portable, and ensure that your application runs consistently across different environments.

---

## What is Docker Compose?
Docker Compose is a tool for defining and running multi-container Docker applications. With a single `docker-compose.yml` file, you can configure all your services (e.g., app, database, cache) and manage them together.

---

## Dockerfile Explained
The `Dockerfile` is a script that contains instructions to build a Docker image for your application. Here’s the `Dockerfile` used in your project:

```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and model code
COPY app/ ./app/
COPY model/ ./model/

# Add PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app

# Expose port (if your app uses one, e.g., Flask)
EXPOSE 5000

# Set entrypoint (adjust if main.py is not the entry)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Explanation of Each Line
1. **`FROM python:3.11-slim`**:
   - Specifies the base image to use. Here, we use a lightweight Python 3.11 image.
   - Best Practice: Use slim images to reduce image size.

2. **`WORKDIR /app`**:
   - Sets the working directory inside the container to `/app`.
   - Best Practice: Always set a working directory to keep files organized.

3. **`COPY requirements.txt ./`**:
   - Copies the `requirements.txt` file from your local machine to the container.

4. **`RUN pip install --no-cache-dir -r requirements.txt`**:
   - Installs Python dependencies listed in `requirements.txt`.
   - Best Practice: Use `--no-cache-dir` to reduce image size.

5. **`COPY app/ ./app/` and `COPY model/ ./model/`**:
   - Copies the `app` and `model` directories into the container.

6. **`ENV PYTHONPATH=/app`**:
   - Adds `/app` to the Python module search path.

7. **`EXPOSE 5000`**:
   - Informs Docker that the container listens on port 5000.
   - Best Practice: Use this for documentation; it doesn’t actually publish the port.

8. **`CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]`**:
   - Specifies the command to run when the container starts.
   - Here, it runs the FastAPI app using Uvicorn.

---

## docker-compose.yml Explained
The `docker-compose.yml` file defines and runs multiple containers. Here’s the file used in your project:

```yaml
version: '3.8'
services:
  app:
    build: .
    container_name: python_app
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app/app
      - ./model:/app/model
    restart: unless-stopped

  redis:
    image: redis:latest
    container_name: redis
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### Explanation of Each Section
1. **`version: '3.8'`**:
   - Specifies the Docker Compose file format version.

2. **`services:`**:
   - Defines the services (containers) to run.

3. **`app:`**:
   - The name of the service for your Python app.

4. **`build: .`**:
   - Builds the Docker image using the `Dockerfile` in the current directory.

5. **`container_name: python_app`**:
   - Sets the name of the container to `python_app`.

6. **`ports:`**:
   - Maps port 5000 on the host to port 5000 in the container.
   - Format: `host_port:container_port`.

7. **`volumes:`**:
   - Mounts local directories into the container for development.
   - Example: `./app:/app/app` syncs the local `app` directory with the container.

8. **`restart: unless-stopped`**:
   - Automatically restarts the container unless it is explicitly stopped.

9. **`redis:`**:
   - Defines the Redis service.

10. **`image: redis:latest`**:
    - Uses the latest Redis image from Docker Hub.

11. **`container_name: redis`**:
    - Sets the name of the Redis container to `redis`.

12. **`ports:`**:
    - Maps port 6379 on the host to port 6379 in the container.

---

## Best Practices
### Dockerfile
- Use slim base images to reduce size.
- Combine `RUN` commands to minimize image layers.
- Use `.dockerignore` to exclude unnecessary files.

### Docker Compose
- Use environment variables for sensitive data (e.g., passwords).
- Use named volumes for persistent data.
- Avoid hardcoding ports; use environment variables.

---

## Important Commands
### Docker Commands
1. **Build an Image**:
   ```bash
   docker build -t my-image .
   ```

2. **Run a Container**:
   ```bash
   docker run -p 5000:5000 my-image
   ```

3. **List Running Containers**:
   ```bash
   docker ps
   ```

4. **Stop a Container**:
   ```bash
   docker stop container_name
   ```

5. **View Logs**:
   ```bash
   docker logs container_name
   ```

### Docker Compose Commands
1. **Start Services**:
   ```bash
   docker-compose up
   ```

2. **Rebuild and Start Services**:
   ```bash
   docker-compose up --build
   ```

3. **Stop Services**:
   ```bash
   docker-compose down
   ```

4. **View Logs**:
   ```bash
   docker-compose logs
   ```

---

This guide should help your students understand the `Dockerfile` and `docker-compose.yml` files, as well as best practices and important commands. Encourage them to experiment and ask questions!