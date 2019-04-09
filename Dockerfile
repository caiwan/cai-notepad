FROM python:3.7-alpine3.9
EXPOSE 3031
# VOLUME /usr/src/app/public
# WORKDIR /usr/src/app

ENV DATABASE="postgresql"
ENV DATABASE_NAME = ""
ENV DATABASE_USER = ""
ENV DATABASE_PASSWORD = ""
ENV DATABASE_HOST = ""
ENV DATABASE_PORT = ""

ENV CSRF_SESSION_KEY = ""

ENV GOOGLE_CLIENT_ID = ""
ENV GOOGLE_CLIENT_SECRET = ""

ADD ./server /app
WORKDIR /app
# COPY --from=static-build /client/dist/* /app/static/
# COPY ./docker/wait-for-it.sh /app/
COPY ./docker/backend/*.sh /app/
COPY ./docker/backend/*.py /app/
COPY ./docker/backend/uwsgi.ini /app/

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
COPY ./docker/backend/uwsgi.ini /app

RUN apk add --no-cache \
  uwsgi-python3 \
  python3
COPY . .
RUN rm -rf public/*
RUN pip3 install --no-cache-dir -r requirements.txt
# CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
#   "--uid", "uwsgi", \
#   "--plugins", "python3", \
#   "--protocol", "uwsgi", \
#   "--wsgi", "main:application" ]

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["/app/start.sh"]
