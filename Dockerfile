FROM python:3.7-alpine
ADD ./server/ /app
WORKDIR /app
COPY ./docker/wait-for-it.sh /app/wait-for-it.sh

RUN apk update \
    && apk add bash \
    && apk add --no-cache --virtual .build-deps \
        bzip2-dev \
        coreutils \
        cython \
        dpkg-dev dpkg \
        expat-dev \
        findutils \
        gcc \
        libc-dev \
        libffi-dev \
        libnsl-dev \
        openssl-dev \
        libtirpc-dev \
        linux-headers \
        make \
        ncurses-dev \
        pax-utils \
        python3-dev \
        util-linux-dev \
        xz-dev \
        zlib-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps

VOLUME /app
CMD ["/app/wait-for-it.sh", "-t", "120", "mongo:27017", "--", "python", "manage.py", "runserver"]
