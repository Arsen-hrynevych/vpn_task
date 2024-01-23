FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /vpn-service

# Copy poetry related files
COPY pyproject.toml /vpn-service/

# Install poetry dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /vpn-service/

# Expose the port
EXPOSE 8000

# Define the command to run your application
CMD ["poetry", "run", "python", "manage.py", "runserver"]
