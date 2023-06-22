FROM python:3.11-bookworm as builder
RUN mkdir /app
WORKDIR /app
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.5.1

RUN curl -sSL https://install.python-poetry.org | python - --version ${POETRY_VERSION}

COPY pyproject.toml poetry.toml poetry.lock README.md /app/
RUN ~/.local/bin/poetry install --no-root --only main --no-interaction --no-directory

COPY sunshine_input_bridge /app/sunshine_input_bridge
RUN ~/.local/bin/poetry install --only main --compile

FROM python:3.11-slim-bookworm as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1
RUN mkdir /app 
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/sunshine_input_bridge ./sunshine_input_bridge
CMD ["./.venv/bin/python", "-m", "sunshine_input_bridge"]

HEALTHCHECK --interval=5s --timeout=30s --start-period=30s --retries=10 CMD ["./.venv/bin/python", "-m", "sunshine_input_bridge", "--healthcheck"]
