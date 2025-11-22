# backend/ai-service/Dockerfile
FROM python:3.11-slim
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential libsndfile1 git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY app /app/app

# Optional: copy model or mount via volume
# COPY model.pt /app/model.pt

EXPOSE 5005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5005", "--reload"]
