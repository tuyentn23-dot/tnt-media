FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
 PIP_NO_CACHE_DIR=1 \
 DEBIAN_FRONTEND=noninteractive \
 PORT=7860 \
 HOST=0.0.0.0

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
 ffmpeg \
 fonts-dejavu-core \
 curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p logs output memory system config

EXPOSE 7860

CMD ["bash", "deploy/start_hf.sh"]
