FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    git \
    curl \
 && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
RUN pip install pytest
RUN pytest tests/

EXPOSE 80

CMD ["gunicorn", "app:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80","--timeout", "60"]
