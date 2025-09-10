FROM python:3.11-slim

WORKDIR /app

COPY services/metadata/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/utils/ ./utils/

COPY services/metadata/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/manager.py"]