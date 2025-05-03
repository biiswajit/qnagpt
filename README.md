qnagpt is an api based web app that can generate questions from pdfs

## required tools

- python [installation guide](https://www.python.org/downloads/)
- uv [installation guide](https://docs.astral.sh/uv/guides/install-python/)

## project setup

1. clone the repository

    ```bash
    # if you have ssh key setup
    git clone git@github.com:biiswajit/qnagpt.git
    # if you don't have ssh key setup
    git clone https://github.com/biiswajit/qnagpt.git
    ```

2. install all the dependencies

    ```bash
    # this command will install all project dependencies
    uv sync
    ```

3. run the server

    ```bash
    uv run fastapi dev
    ```

    once the command is running the api server can be found on following endpoints

    ```bash
    # for api server
    http://127.0.0.1:8000
    # for api documentation site
    http://127.0.0.1:8000/docs
    ```