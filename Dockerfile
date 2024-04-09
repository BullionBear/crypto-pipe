# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /scheduler

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV MONGO_URL mongodb://localhost:27017

COPY . /scheduler

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
