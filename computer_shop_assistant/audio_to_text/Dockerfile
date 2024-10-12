# Dockerfile for audio_to_text_service

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY audio_to_text_service.py .

CMD ["gunicorn", "-b", "0.0.0.0:5001", "audio_to_text_service:app"]