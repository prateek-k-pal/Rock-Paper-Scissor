# Use Python 3.10 as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by pygame
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages directly
RUN pip install --no-cache-dir pygame

# Copy the rest of the application code into the container
COPY . .

# Make port 5555 available to the world outside this container
EXPOSE 5555

# Define environment variable (if needed for your server)
ENV PYTHONUNBUFFERED=1

# Run the application (assuming your script is named server.py)
CMD ["python", "server.py"]
