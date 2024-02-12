FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY . ./

ENV PYTHONPATH=./
ENV PYTHONUNBUFFERED=True
EXPOSE "$LISTEN_PORT"

RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

RUN python -m ensurepip --upgrade && pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE $LISTEN_PORT

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
