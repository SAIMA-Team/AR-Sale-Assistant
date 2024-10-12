FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY select_animation_service.py .

CMD ["gunicorn", "-b", "0.0.0.0:5004", "select_animation_service:app"]