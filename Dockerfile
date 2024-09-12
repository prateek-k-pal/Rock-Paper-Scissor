# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Install system dependencies required for Pygame
RUN apt-get update && \
    apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev libjpeg-dev libtiff-dev libpng-dev && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy your requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your app's code
COPY . .

# Expose the port that Flask will use
EXPOSE 5555

# Start the Flask app
CMD ["python", "server.py"]
