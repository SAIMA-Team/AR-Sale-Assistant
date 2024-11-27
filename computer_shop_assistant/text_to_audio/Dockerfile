FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Update the package manager and install ffmpeg and espeak
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask application code into the container
COPY text_to_audio_service.py .

# Expose the port your service will run on
EXPOSE 5002

# Command to run your Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5002", "text_to_audio_service:app"]
