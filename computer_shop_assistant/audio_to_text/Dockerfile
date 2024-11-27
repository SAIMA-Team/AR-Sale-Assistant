# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY audio_to_text_service.py .

# Expose port 5001 for the Flask app
EXPOSE 5001

# Start the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5001", "audio_to_text_service:app"]
