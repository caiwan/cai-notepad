# Build static html packages w/ NPM
FROM node:11-alpine as static-build
RUN apk update && apk add bash
ADD ./client /client
WORKDIR /client
RUN npm install && \
  npm run build

# Application
FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7

ENV NGINX_MAX_UPLOAD 0
ENV LISTEN_PORT 8001
ENV UWSGI_INI /app/uwsgi.ini
ENV STATIC_URL /
ENV STATIC_PATH /app/static

# copy and configure app
ADD ./server /app
WORKDIR /app
COPY --from=static-build /client/dist/* /app/static/
COPY ./docker/wait-for-it.sh /app/
COPY ./docker/entrypoint.sh /app/
COPY ./docker/uwsgi.ini /app/

# --- Install py deps
USER root
RUN apk update \
  && apk add bash \
  && apk add --no-cache --virtual .build-deps \
    bzip2-dev \
    coreutils \
    dpkg-dev dpkg \
    expat-dev \
    findutils \
    gcc \
    gdbm-dev \
    libc-dev \
    libffi-dev \
    libnsl-dev \
    openssl-dev \
    libtirpc-dev \
    linux-headers \
    make \
    ncurses-dev \
    pax-utils \
    readline-dev \
    sqlite-dev \
    tcl-dev \
    tk \
    tk-dev \
    util-linux-dev \
    xz-dev \
    zlib-dev \
    python3-dev \
    cython \
  && pip install --upgrade pip \
  && pip install --upgrade cython \
  && pip install uwsgi \
  && pip install -r requirements.txt \
  && apk del .build-deps

# --- Config uWSGI
COPY ./docker/uwsgi.ini /app

# --- entrypoint
COPY ./docker/entrypoint.sh /app/
COPY ./docker/start.sh /app/
COPY ./docker/prestart.sh /app/
RUN chmod +x /app/entrypoint.sh \
  /app/start.sh \
  /app/prestart.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["/app/start.sh]
