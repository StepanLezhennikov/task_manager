FROM python:3.12-slim as builder

LABEL authors="Stepan Lezhennikov"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --verbose

FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache bash gcc libpq-dev

WORKDIR /app

COPY --from=builder /app /app

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --verbose

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

COPY entrypoint.sh /entrypoint.sh
COPY worker_entrypoint.sh /worker_entrypoint.sh

RUN chmod +x /entrypoint.sh /worker_entrypoint.sh

RUN chown -R appuser:appgroup /entrypoint.sh /worker_entrypoint.sh

USER appuser

EXPOSE 8000

CMD ["/entrypoint.sh"]
