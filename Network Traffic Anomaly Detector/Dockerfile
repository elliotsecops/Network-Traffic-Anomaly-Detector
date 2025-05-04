# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
# This layer will only be rebuilt if requirements.txt changes
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This layer will be rebuilt if any other file changes
COPY . .

# Create the logs directory
# This ensures the directory exists and the default user has write permissions
RUN mkdir logs

# Expose any ports if necessary (e.g., if the application had a web interface)
# EXPOSE 8000

# Command to run the application when the container starts
CMD ["python", "main.py"]
