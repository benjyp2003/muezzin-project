FROM python:3.11-slim

WORKDIR /app

COPY metadata/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/ ./utils/

COPY metadata/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/manager.py"]