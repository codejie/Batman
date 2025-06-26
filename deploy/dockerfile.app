FROM alpine/git:v2.49.0 AS clone

RUN git clone --branch v0.3 --depth 1 https://github.com/codejie/Batman.git /batman

FROM python:3.13.5-slim AS backend
COPY --from=clone /batman /batman

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr/local \
    && make \
    && make install

RUN ln -s /usr/local/lib/libta_lib.a /usr/local/lib/libta-lib.a

WORKDIR /batman/app
RUN pip install --no-cache-dir -r requirements_docker.txt uvicorn

RUN rm -rf /ta-lib-0.4.0-src.tar.gz /ta-lib
RUN apt-get remove -y \
    build-essential \
    wget \
    && apt-get autoremove -y \
    && apt-get clean
RUN rm -rf /batman/.git

VOLUME /batman/app/db
EXPOSE 8000

WORKDIR /batman
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]