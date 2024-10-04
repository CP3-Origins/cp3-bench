# Methods to install, default all
ARG METHODS="all"

# Get the base image
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

# Set methods value
ARG METHODS

# Alias python to python3
RUN echo "alias python=python3" >> ~/.bashrc

# Set sudo
RUN apt-get update && apt-get install -y sudo

# System setup and dependencies
RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
    git \
    wget \
    python3-dev \
    pip \
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
RUN curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
RUN echo >> /root/.bashrc
RUN echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /root/.bashrc
RUN eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"

# Install pyenv
RUN brew install pyenv
RUN brew install pyenv-virtualenv 

# Set paths
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init  -)"' >> ~/.bashrc

# Install cp3-methods
RUN python3 ./bench/install.py --methods $METHODS
