FROM python:3.11-slim

WORKDIR /app

COPY services/text_analyzer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/utils/ ./utils/

COPY services/text_analyzer/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/manager.py"]