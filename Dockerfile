FROM python:3.9.10-bullseye AS build

ENV APP_NAME="spoty"
ENV VENV_PATH="/opt/venvs/$APP_NAME"
ENV PATH="$VENV_PATH/bin:$PATH"

COPY requirements.txt .

RUN python3 -m venv $VENV_PATH && \
    pip install -r requirements.txt

FROM python:3.9.10-slim-bullseye AS virtualenv

ENV APP_NAME="spoty"
ENV VENV_PATH="/opt/venvs/$APP_NAME"

COPY --from=build $VENV_PATH $VENV_PATH

FROM virtualenv AS base

ENV APP_NAME="spoty"
ENV VENV_PATH="/opt/venvs/$APP_NAME"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

ENV USERNAME=app
RUN useradd -u 8877 $USERNAME
WORKDIR "/$APP_NAME"

RUN chown -R ${USERNAME} "/$APP_NAME"
USER ${USERNAME}

COPY . .

FROM virtualenv AS dev

ARG USERNAME=spoty
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV APP_NAME="spoty"
ENV VENV_PATH="/opt/venvs/$APP_NAME"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

COPY requirements-dev.txt .

RUN apt-get update && \
    apt-get install git make -y && \
    echo "umask 002" | tee -a /etc/bash.bashrc /etc/profile && \
    pip install --upgrade pip && \
    pip install -r requirements-dev.txt && \
    groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -d "/home/$USERNAME" -m -k /etc/skel ${USERNAME}

USER ${USERNAME}
