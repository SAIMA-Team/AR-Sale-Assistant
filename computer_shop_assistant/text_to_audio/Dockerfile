FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY text_to_audio_service.py .

CMD ["gunicorn", "-b", "0.0.0.0:5002", "text_to_audio_service:app"]