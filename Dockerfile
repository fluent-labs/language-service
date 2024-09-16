FROM python:3.9.10-alpine3.15 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev

RUN pip install "poetry==$POETRY_VERSION"

RUN python -m venv /venv

# This is needed because pkuseg has an undeclared install time dependency for numpy. 
RUN /venv/bin/pip install numpy==1.22.0

COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry run pytest
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

# Make sure gunicorn is on the path
ENV PATH="/venv/bin:${PATH}"

COPY --from=builder /venv /venv
COPY language_service /app/

EXPOSE 8000
CMD ["gunicorn", "LanguageService:app", "--config=gunicorn.conf.py"]
