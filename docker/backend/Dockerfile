FROM python:3.7-alpine3.9 as pybase

WORKDIR /
COPY ./server/requirements.txt /

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

# ---

FROM pybase

EXPOSE 3031
# VOLUME /usr/src/app/public
# WORKDIR /usr/src/app

ENV DATABASE="postgresql"
ENV DATABASE_NAME="notesapp"
ENV DATABASE_USER="notesappuser"
ENV DATABASE_PASSWORD="notesapppassword"
ENV DATABASE_HOST="database"
ENV DATABASE_PORT="5432"
ENV CSRF_SESSION_KEY=""
ENV GOOGLE_CLIENT_ID=""
ENV GOOGLE_CLIENT_SECRET=""
ENV DEFAULT_USER="USER"
ENV DEFAULT_USER="PASSWORD"

ADD ./server /app
WORKDIR /app
COPY ./docker/backend/*.sh /app/
COPY ./docker/backend/*.py /app/
COPY ./docker/backend/uwsgi.ini /app/

# --- Config uWSGI
COPY ./docker/backend/uwsgi.ini /app

RUN apk add --no-cache \
  uwsgi-python3 \
  python3
COPY . .
RUN rm -rf public/*
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["sh", "/app/start.sh"]
