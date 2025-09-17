FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install --upgrade pip wheel poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

# Copy application source and configs (needed for running the app and alembic)
COPY . .

RUN chmod +x deployment/run

ENTRYPOINT ["./deployment/run"]