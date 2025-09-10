FROM python:3.11-slim


WORKDIR /app
COPY services/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/utils/ ./utils/

COPY services/api/ ./

WORKDIR /app/app
ENV PYTHONPATH=/app
CMD ["python", "app/main.py"]