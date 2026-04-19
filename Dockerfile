FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY monitor.py .
COPY config.ini .

# Add this line — fixes the buffering issue on Windows/Docker
ENV PYTHONUNBUFFERED=1

CMD ["python", "monitor.py"]