# Docker Context

- Docker detected: `False`
- Dockerfile lines: `26`
- Base image: `python:3.10-slim`

## Dockerfile Preview

- FROM python:3.10-slim
- 
- WORKDIR /app
- 
- ENV PYTHONDONTWRITEBYTECODE=1
- ENV PYTHONUNBUFFERED=1
- ENV MPLCONFIGDIR=/tmp/matplotlib
- 
- RUN apt-get update && apt-get install -y --no-install-recommends \
-     build-essential \
-     libgl1 \
-     libglib2.0-0 \