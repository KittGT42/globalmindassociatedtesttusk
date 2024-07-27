# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install

# Copy the rest of the application code to the container
COPY . /app/

# Specify the command to run the application
CMD ["poetry", "run", "python", "main.py"]
