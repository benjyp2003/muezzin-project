FROM python:3.11-slim

WORKDIR /app

COPY speech_to_text/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY utils/ ./utils/

COPY speech_to_text/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/controller/manager.py"]