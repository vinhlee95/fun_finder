# Use the official Python image from the Docker Hub
FROM python:3.12.7-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the rest of the application code into the container
COPY . .

# Make the entry point script executable
RUN chmod +x ./entrypoint.sh

# Expose the port that the app runs on
EXPOSE 8080

# Run the server
CMD uvicorn app:app --host 0.0.0.0 --port 8080

# Set the entry point to the custom script
# ENTRYPOINT ["./entrypoint.sh"]
