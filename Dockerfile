# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Create the full directory structure
RUN mkdir -p /app/beta/python/No.1

# Copy the entire project
COPY . /app

# Create __init__.py files to make directories Python packages
RUN touch /app/__init__.py
RUN touch /app/beta/__init__.py
RUN touch /app/beta/python/__init__.py
RUN touch /app/beta/python/No.1/__init__.py

# Install dependencies
COPY beta/python/No.1/requirements.txt /app/beta/python/No.1/requirements.txt
RUN pip install --no-cache-dir -r /app/beta/python/No.1/requirements.txt
RUN pip install gunicorn

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PORT=8050

# Expose the port the app runs on
EXPOSE 8050

# Modify main.py to explicitly expose server
RUN sed -i '1iimport sys\nsys.path.append("/app")' /app/beta/python/No.1/main.py

# Use a wrapper script for more control
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
