# syntax=docker/dockerfile:1.7

# Stage 1: Build dependencies using the full python image for better compatibility
FROM python:3.12 AS builder
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com \
    PIP_DEFAULT_TIMEOUT=600 \
    PIP_RETRIES=10

# Change to a faster mirror and install build-time OS dependencies
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*
    
# Download, compile, and install ta-lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz\
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr/local --build=`/bin/arch`-unknown-linux-gnu \
    && make \
    && make install

# Create a virtual environment and install Python packages
COPY app/requirements_docker.txt /app/requirements_docker.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN --mount=type=cache,id=batman-pip-cache,target=/root/.cache/pip \
    pip install -r /app/requirements_docker.txt

# Stage 2: Create the final, lightweight production image using the slim version
FROM python:3.12-slim

# Change to a faster mirror and install only runtime OS dependencies
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the compiled ta-lib library and the venv from the builder stage
COPY --from=builder /usr/local/lib/libta_lib* /usr/local/lib/
COPY --from=builder /opt/venv /opt/venv

# Copy only the backend application code, not the entire repo
COPY app /batman/app

# Set the PATH to use the virtual environment and define runtime variables
ENV PATH="/opt/venv/bin:$PATH"
ENV HOST="0.0.0.0"
ENV PORT="8000"
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

VOLUME /batman/app/db
EXPOSE ${PORT}

# Set up the application directory
WORKDIR /batman
CMD ["sh", "-c", "exec uvicorn app.main:app --host $HOST --port $PORT"]
