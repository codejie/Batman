FROM python:3.12-slim-bullseye

# 安装系统依赖
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    wget \
    git \
    sqlite3 \
    curl \
    && curl -sL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && make clean

WORKDIR /usr/local/lib
RUN ln -s libta_lib.a libta-lib.a
RUN ln -s libta_lib.so libta-lib.so

RUN git clone --depth 1 https://github.com/codejie/Batman.git /batman

# 设置Python
WORKDIR /batman/app
RUN pip install --no-cache-dir -r requirements_docker.txt uvicorn

# 设置pnpm
WORKDIR /batman/signal
RUN npm install -g pnpm
RUN npm install -g serve

RUN pnpm i
RUN pnpm run build:pro

# 清理
RUN rm -rf /ta-lib-0.4.0-src.tar.gz /ta-lib
RUN rm -rf /batman/.git
RUN rm -rf /batman/signal/node_modules
RUN apt-get remove -y \
    build-essential \
    wget \
    git \
    curl \
    && apt-get autoremove -y \
    && apt-get clean

# 执行
VOLUME /batman/app/db
EXPOSE 3030 8000

WORKDIR /batman

CMD ["sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    serve -s ./signal/dist-pro -l 3030"]
