# BUILDER STAGE
FROM python:3.10-slim-buster AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# FINAL STAGE
FROM python:3.10-slim-buster

WORKDIR /app

# Copy only the wheels from the builder stage
COPY --from=builder /app/wheels /app/wheels

# Copy the necessary project files
COPY ./backend /app/backend
COPY ./data /app/data

RUN pip install --no-cache /app/wheels/*

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
