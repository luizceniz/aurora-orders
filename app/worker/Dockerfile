FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# No dependencies yet: the Redis client arrives in Module 2.
COPY worker.py .

RUN useradd --uid 10001 --no-create-home app
USER 10001

# Exec form (JSON array): Python runs as PID 1 and receives SIGTERM directly.
CMD ["python", "worker.py"]
