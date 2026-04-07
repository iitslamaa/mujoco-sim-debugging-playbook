FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MPLCONFIGDIR=/tmp/matplotlib

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY scripts /app/scripts
COPY configs /app/configs
COPY docs /app/docs
COPY cases /app/cases
COPY outputs /app/outputs

RUN pip install --upgrade pip setuptools wheel && \
    pip install -e . --no-build-isolation

CMD ["python", "scripts/smoke_test.py"]
