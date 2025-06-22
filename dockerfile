# 第一阶段：构建Python后端
FROM python:3.13.5-slim AS backend

# 安装系统依赖 (包括TA-Lib依赖)
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    wget \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 安装TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install

# 克隆后端代码并安装依赖
RUN git clone --branch v0.3 https://github.com/codejie/Batman.git /app/source

# 设置工作目录并安装Python依赖
WORKDIR /app/source/app
RUN pip install --no-cache-dir -r requirements_docker.txt uvicorn

# 第二阶段：构建Node.js前端
FROM node:22.16.0-alpine3.22 AS frontend

# 安装pnpm
RUN npm install -g pnpm

# 克隆前端代码
# RUN git clone https://github.com/your-repo/frontend.git /app/frontend
WORKDIR /app/source/signal

# 安装依赖并构建
COPY --from=backend /app/source/signal /app/signal
RUN pnpm run i
RUN pnpm run build:pro

# 第三阶段：最终运行时
FROM python:3.13.5-slim

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    libgomp1 \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 复制后端应用
COPY --from=backend /usr/lib/libta_lib* /usr/lib/
COPY --from=backend /app/source/app /app/app
WORKDIR /app/app

# 复制前端构建产物
COPY --from=frontend /app/source/signal/dist-pro /app/signal/dist

# 安装前端服务工具
RUN pip install --no-cache-dir serve

# 暴露端口
EXPOSE 8000 3000

# 启动脚本
CMD ["sh", "-c", \
    "serve -s /app/signal/dist -l 3000 & \
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]
