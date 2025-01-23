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

# Create a directory structure
RUN mkdir -p /app/beta/python/No.1

# Copy requirements and install dependencies
COPY beta/python/No.1/requirements.txt /app/beta/python/No.1/requirements.txt
RUN pip install --no-cache-dir -r /app/beta/python/No.1/requirements.txt
RUN pip install gunicorn

# Copy the entire project
COPY . /app

# Create an empty __init__.py files to make directories Python packages
RUN touch /app/__init__.py
RUN touch /app/beta/__init__.py
RUN touch /app/beta/python/__init__.py
RUN touch /app/beta/python/No.1/__init__.py

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8050

# Expose the port the app runs on
EXPOSE 8050

# Modify the gunicorn command to use the correct import path
CMD ["gunicorn", \
     "--chdir", "/app", \
     "--bind", "0.0.0.0:8050", \
     "beta.python.No.1.main:server"]
