FROM python:3.11.0b3-slim-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
        apt-get install -y --no-install-recommends libgmp10=2:6.2.1+dfsg-1+deb11u1 && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

FROM base as builder

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get update && \
        apt-get install -y --no-install-recommends apt-utils=2.2.4 && \
        apt-get install -y --no-install-recommends build-essential=12.9

RUN python -m venv /venv

# This is needed because pkuseg has an undeclared install time dependency for numpy. 
RUN /venv/bin/pip install numpy==1.22.0

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

# Make sure gunicorn is on the path
ENV PATH="/venv/bin:${PATH}"

COPY --from=builder /venv /venv
COPY language_service /app/

EXPOSE 8000
CMD ["gunicorn", "LanguageService:app", "--config=gunicorn.conf.py"]
