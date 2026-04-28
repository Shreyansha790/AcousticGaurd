FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY edge_sensor_bridge.py ./

ENV PYTHONUNBUFFERED=1

# Cloud Run / Cloud Functions inject GOOGLE_APPLICATION_CREDENTIALS and
# FIREBASE_DATABASE_URL via env. The script auto-discovers them.
ENTRYPOINT ["python", "edge_sensor_bridge.py"]
