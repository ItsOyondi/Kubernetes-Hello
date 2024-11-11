# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
