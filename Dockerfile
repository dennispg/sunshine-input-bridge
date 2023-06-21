FROM python:3.11-slim-bookworm as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1
RUN mkdir /app 
WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1

RUN apt-get update \
    && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python - --version ${POETRY_VERSION}

COPY pyproject.toml poetry.toml poetry.lock /app/
RUN poetry install --no-root --no-dev --no-interaction --no-directory

COPY /sunshine_input /app
RUN poetry install --no-dev --compile

FROM base as final
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist .
CMD ["./.venv/bin/python", ""]

HEALTHCHECK --interval=5s --timeout=30s --start-period=30s --retries=10 CMD [ "executable" ]