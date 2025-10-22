FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl wget ffmpeg unzip fonts-liberation libnss3 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libgtk-3-0 \
    libasound2 libxshmfence1 libgbm1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
RUN python -m playwright install --with-deps

COPY app /app
WORKDIR /app

EXPOSE 8080

CMD ["python", "server.py"]