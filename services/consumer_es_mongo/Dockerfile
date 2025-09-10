FROM python:3.11-slim


WORKDIR /app
COPY consumer_es_mongo/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/ ./utils/

COPY consumer_es_mongo/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/controller/manager.py"]