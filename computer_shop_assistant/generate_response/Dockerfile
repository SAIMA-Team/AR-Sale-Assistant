FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY generate_response_service.py .

CMD ["gunicorn", "-b", "0.0.0.0:5003", "generate_response_service:app"]