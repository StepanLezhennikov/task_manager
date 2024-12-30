FROM python:3.12-slim as builder

LABEL authors="Stepan Lezhennikov"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache bash gcc libpq-dev
COPY --from=builder /app .

RUN pip install --upgrade pip && pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY entrypoint.sh /entrypoint.sh
COPY worker_entrypoint.sh /worker_entrypoint.sh

RUN chmod +x /entrypoint.sh /worker_entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["/entrypoint.sh"]
