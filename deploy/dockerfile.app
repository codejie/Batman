# Stage 1: Clone the repository (No changes here)
FROM alpine/git:v2.49.0 AS clone
RUN git clone --branch master --single-branch --depth=1 https://github.com/codejie/Batman.git /batman

# Stage 2: Build dependencies in a dedicated builder stage
FROM python:3.13-slim AS builder

# 设置 DNS（可选，解决 DNS 解析问题）
# RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# 替换为清华大学镜像源
RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian bookworm main contrib non-free" > /etc/apt/sources.list \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# Install build-time OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*
    
# Download, compile, and install ta-lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz\
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr/local \
    && make \
    && make install

# Create a virtual environment and install Python packages
COPY --from=clone /batman/app/requirements_docker.txt /app/requirements_docker.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r /app/requirements_docker.txt uvicorn

# Stage 3: Create the final, lightweight production image
FROM python:3.13-slim
# Install only runtime OS dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the compiled ta-lib library from the builder stage
COPY --from=builder /usr/local/lib/libta_lib* /usr/local/lib/
# Copy the virtual environment with installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv
# Copy the application code from the clone stage
COPY --from=clone /batman /batman

# Set the PATH to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV HOST="0.0.0.0"
ENV PORT="8000"

VOLUME /batman/app/db
EXPOSE ${PORT}

WORKDIR /batman
CMD ["sh", "-c", "uvicorn app.main:app --host $HOST --port $PORT"]
