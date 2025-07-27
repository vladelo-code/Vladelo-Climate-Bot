FROM python:3.11-slim

LABEL authors="vladelo"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["python", "app/main.py"]

