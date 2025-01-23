# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip

# Install project dependencies
RUN pip install --no-cache-dir \
    dash \
    dash-bootstrap-components \
    pandas \
    gunicorn

# Alternatively, if you have a requirements.txt file
RUN pip install --no-cache-dir -r beta/python/No.1/requirements.txt

# Expose the port the app runs on
EXPOSE 8050

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DASH_DEBUG=False

# Command to run the application
CMD ["python3", "beta/python/No.1/main.py"]

# Optional: If you want to use gunicorn for production
# CMD ["gunicorn", "--bind", "0.0.0.0:8050", "beta.python.No.1.main:app.server"]
