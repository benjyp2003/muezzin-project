FROM python:3.11-slim

WORKDIR /app

COPY services/speech_to_text/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/utils/ ./utils/

COPY services/speech_to_text/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/controller/manager.py"]