# Methods to install, default all
ARG METHODS="dsr"

# Use an official Python runtime as a parent image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Set methods value
ARG METHODS

# Set sudo
RUN apt-get update && apt-get install -y sudo

# System setup and dependencies
RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
    git \
    nano\
    ssh-client \
    software-properties-common \
    build-essential \
    ca-certificates \
    libpq-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
  && apt-get clean

# Set the working directory in the container and root environment variable
ENV HOME="/root"
WORKDIR ${HOME}

# Copy the current directory contents into the container at /root
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install brew
RUN export HOMEBREW_NO_INSTALL_FROM_API=1
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install pyenv
#RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
#RUN git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
RUN brew update
RUN brew install pyenv
RUN brew install pyenv-virtualenv \

ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init  -)"' >> ~/.bashrc

# Install cp3-methods
#RUN eval "$(pyenv init -)"
#RUN eval "$(pyenv virtualenv-init -)"
#RUN python ./bench/install.py --methods $METHODS

# Initialize again
#RUN eval "$(pyenv init -)"
#RUN eval "$(pyenv virtualenv-init -)"
