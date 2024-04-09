# Use the official Python image from the Docker Hub
FROM python:3.11.9-bullseye

# Set the working directory in the container
WORKDIR /scheduler

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /scheduler

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
