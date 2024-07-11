# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /usr/src

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* ./

# Install the dependencies
RUN poetry install --no-root

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run uvicorn server with --reload
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]