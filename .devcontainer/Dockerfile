FROM ubuntu:26.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    black \
    ca-certificates \
    cmake \
    curl \
    g++ \
    git \
    make \
    nano \
    openssh-client \
    python3 \
    sudo \
    && rm -rf /var/lib/apt/lists/*

ARG BAZELISK_VERSION=1.30.0
ADD https://github.com/bazelbuild/bazelisk/releases/download/v${BAZELISK_VERSION}/bazelisk-linux-amd64 /usr/local/bin/bazel
RUN chmod +x /usr/local/bin/bazel

ARG BUILDIFIER_VERSION=8.0.3
ADD https://github.com/bazelbuild/buildtools/releases/download/v${BUILDIFIER_VERSION}/buildifier-linux-amd64 /usr/local/bin/buildifier
RUN chmod +x /usr/local/bin/buildifier

ARG USERNAME=ubuntu
RUN passwd -d ${USERNAME} \
    && mkdir -p /home/${USERNAME}/.cache && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.cache \
    && SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/home/${USERNAME}/.cache/.bash_history" \
    && echo "$SNIPPET" >> "/home/${USERNAME}/.bash_aliases"

USER ${USERNAME}

WORKDIR /workspace
