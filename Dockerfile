# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies specified in requirements.txt
# If you have any requirements, make sure to include a requirements.txt file
# and uncomment the following line
# COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Python script
CMD ["python", "main.py"]
