FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main_orchestrator.py .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main_orchestrator:app"]