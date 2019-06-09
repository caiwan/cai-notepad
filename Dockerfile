

FROM python:3.7-alpine3.9 as server-base

WORKDIR /
COPY ./backend/requirements.txt /

# --- Install py deps
ENV NGINX_VERSION 1.15.12

USER root
# TODO: Remove unnesesarry packages
RUN apk update \
  && apk add bash \
  && apk add --no-cache --virtual .build-deps \
  curl \
  cython \
  bzip2-dev \
  coreutils \
  dpkg-dev dpkg \
  expat-dev \
  findutils \
  geoip-dev \
  gcc \
  gdbm-dev \
  libc-dev \
  libffi-dev \
  libnsl-dev \
  libtirpc-dev \
  linux-headers \
  libxslt-dev \
  gd-dev \
  gnupg1 \
  make \
  ncurses-dev \
  openssl-dev \
  pax-utils \
  pcre-dev \
  python3-dev \
  readline-dev \
  sqlite-dev \
  tcl-dev \
  tk \
  tk-dev \
  util-linux-dev \
  xz-dev \
  zlib-dev
RUN pip install --upgrade pip \
  && pip install --upgrade cython \
  && pip install uwsgi
RUN apk add \
  pcre \
  libxml2 \
  postgresql-dev \
  libpq
RUN pip install -r requirements.txt \
  && apk add --update supervisor \
  && rm -rf /tmp/* /var/cache/apk/*
RUN apk del .build-deps

# ---

FROM server-base

EXPOSE 3031

ENV DEFAULT_USER="admin"
ENV DEFAULT_PASSWORD="admin"
# - SQLITE by default
ENV DATABASE="sqlite"
ENV DATABASE_NAME=""
ENV DATABASE_USER=""
ENV DATABASE_PASSWORD=""
ENV DATABASE_PATH="notes.db"
# - POSTGRESQL
# ENV DATABASE="postgresql"
# ENV DATABASE_NAME="notesapp"
# ENV DATABASE_USER="notesappuser"
# ENV DATABASE_PASSWORD="notesapppassword"
# ENV DATABASE_HOST="database"
# ENV DATABASE_PORT="5432"
# -- Max timeout for wait-for-it in sec
ENV DATABASE_WAIT_TIMEOUT=380

ENV CSRF_SESSION_KEY=""
ENV GOOGLE_CLIENT_ID=""
ENV GOOGLE_CLIENT_SECRET=""
ENV DEFAULT_USER="USER"
ENV DEFAULT_PASSWORD="PASSWORD"

# Use for debugging inside the docker image
# ENV FLASK_ENV=production
# ENV FLASK_DEBUG=True
# # ENV FLASK_TESTING=False

ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
# ENV FLASK_TESTING=False

ADD ./backend /app
WORKDIR /app
COPY ./docker/*.sh /app/
RUN chmod +x /app/*.sh
COPY ./docker/config /app/config

# --- Config services
COPY ./docker/uwsgi.ini /app/
COPY ./docker/supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["bash", "/app/entrypoint.sh"]
