# Use an official Python runtime
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project directory
COPY beta/python/No.1 /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8050

# Expose the port
EXPOSE 8050

# Create a wsgi.py file to properly expose the server
RUN echo "from app import app as application" > wsgi.py

# Use explicit gunicorn command
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--log-level", "debug", "wsgi:application.server"]
