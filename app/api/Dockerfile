FROM python:3.12-slim

# Python behaves better in containers with these two settings:
# no .pyc files, and logs flushed immediately so `kubectl logs` shows them in real time.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first: this layer is cached and only rebuilt when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The code goes INSIDE the image. No volume, no git pull on the server.
COPY main.py .

# Never run as root inside the container.
RUN useradd --uid 10001 --no-create-home app
USER 10001

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
