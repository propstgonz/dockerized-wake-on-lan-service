FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y etherwake iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY wakeonlan.py /app/wakeonlan.py

WORKDIR /app

CMD ["python", "wakeonlan.py"]
