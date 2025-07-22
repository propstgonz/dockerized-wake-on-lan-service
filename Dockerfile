FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y etherwake iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY wake_on_lan_server.py /app/wake_on_lan_server.py

WORKDIR /app

CMD ["python", "wake_on_lan_server.py"]
