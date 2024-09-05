# Use the official Python image
FROM python:3.9-slim

# Set a working directory
WORKDIR /usr/src/app

# Copy the requirements file (if needed)
COPY requirements.txt .

# Install necessary Python libraries (including kafka-python)
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY . .

# Command to run the Python script
CMD ["python3"]