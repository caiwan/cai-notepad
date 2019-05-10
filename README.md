# Cai-Notes

Yet another self-hosted note taking app and TODO list manager.

**This version is at pre-alpha version at the moment**

## Setup for hosting

For development instructions see below.

### Using Docker

1. Prerequisites

    Install `docker` and `docker-compose`.
    See official instructions for installation of
    [Docker](https://www.docker.com/get-started) and
    [Compose](https://docs.docker.com/compose/install/).

2. Create docker image

    - run `docker-compose up`
    - or to detach it right away to run it in the background `docker-compose up -d`

    For further configuration see `docker-compose.yaml` and
    `Dockerimage` files in the source root, and other configuration
    files in `docker/` folder. Detailed in [docker.md](docker.md).

    Note that you also can create your individual Docker images via

    - `dokcer build -t notes-backend -f docker/backend/Dockerfile .`
    - `dokcer build -t notes-frontend -f docker/frontend/Dockerfile .`


### Manual setup

  TBD



1. Prerequisites

    To build manually you'll need the following packages installed:

    - **Python 3.7** and **pip 18.1** (optionally within a virtual environment) for backend
    - **Node 11.7** and **NPM 6.5** for client (frontend)
    - **uWSGI** via pip for hosting the backend code
    - **nginx** for delegate it to be accessible via http

1. Build client (frontend)

    ```bash
    cd client
    npm i && npm build
    cd ..
    ```

2. Install server dependencies

    ```bash
    cd server
    pip install Cython && pip install -r requirements.txt
    cd ..
    ```

3. Copy static files from client

  ```bash
  cp client/dist server/static
  ```

3. Install and Configure Nginx:

  TBD

3. Configure your server with uWSGI

  ```bash
  cp ./docker/uwsgi.ini /server/wusgi.ini
```

See Flask's [uWSGI documentation](http://flask.pocoo.org/docs/1.0/deploying/uwsgi/) for further details

3. Configure your server app

  - Take `./server/app/config/base.py`
  - For dev and debugging the app loads `./server/app/config/local.py` for it's config
  - For production the app loads `./server/app/config/prodction.py`

4. Run the server with uwsgi:

  ***TODO:*** *This needs to be defined and tested well*

  ```bash
  uwsgi -s /tmp/notes.sock --manage-script-name --mount /notes=server:app
  ```

## Features

TBD, See `SPECS.md` for rough details


## Setup and launching app for development

1. Prerequisites

  To build manually you'll need the following packages installed:

  - **Python 3.7** and **pip 18.1** (optionally within a virtual environment) for backend
  - **Node 11.7** and **NPM 6.5** for client (frontend)

2. Start client (frontend)

  ```bash
  cd client
  npm i
  npm run dev
  ```

3. Start server (backend)

  Install all the dependencies:

  ```bash
  cd server
  pip install Cython && pip install -r requirements.txt && pip install -r requirements-dev.txt
  python manage,py createdb
  cp dev.env .env
  python manage.py runserver
  ```

4. Integrated Development Environment

  We prefer Visual Studio code. Therefore an environemnt config is already supplied with the repo, altogether with different `.*rc` files. The following configuration / linting and quality tools are used:

  - **flake8** (Recommended VSCode plugins: Python, Test Explorer UI, Python Test Explorer)
  - **eslint** (Recommended VSCode plugins: vue, vetur, eslint, beautifyrc)
  - **editorconfig** (Recommended VSCode plugins: editorconfig)

## Contribution

Any contribution ot this project is welcomed, and appreciated, however
there isn't any developer guideline set at this moment.

- For python static code analysis an style check we use `flake8`, ~~however it's not fully configured~~.

## Running tests

Make sure that requirements for development has been installed `pip install -r requirements-dev.txt`

1. Server (backend)

    ```bash
    cd server/
    python tests.py
    ```

2. Client (frontend)
    - There's none ATM

### Future development

TBD

### Known issues

- On some enviromnent live reload of the backend app simply doens't work, and stuck.
- DB restore script doesn't work due foreign key issues on insertion.
