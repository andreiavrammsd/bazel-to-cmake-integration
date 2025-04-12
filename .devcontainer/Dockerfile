FROM ubuntu:24.04

ARG BAZEL_VERSION=7.6.1
ARG BUILDIFIER_VERSION=8.0.3
ARG USERNAME=ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    apt-transport-https \
    bash-completion \
    black \
    ca-certificates \
    cmake \
    curl \
    g++ \
    gcc \
    git \
    gnupg \
    make \
    nano \
    openjdk-17-jdk \
    software-properties-common \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > /usr/share/keyrings/bazel-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list \
    && apt-get update && apt-get install -y bazel-${BAZEL_VERSION} \
    && ln -s /usr/bin/bazel-${BAZEL_VERSION} /usr/bin/bazel \
    && rm -rf /var/lib/apt/lists/*

ADD https://github.com/bazelbuild/buildtools/releases/download/v${BUILDIFIER_VERSION}/buildifier-linux-amd64 /usr/local/bin/buildifier
RUN chmod +x /usr/local/bin/buildifier

RUN passwd -d ${USERNAME} \
    && mkdir -p /home/${USERNAME}/.cache && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.cache \
    && SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/home/${USERNAME}/.cache/.bash_history" \
    && echo "$SNIPPET" >> "/home/${USERNAME}/.bash_aliases"

USER ${USERNAME}

WORKDIR /workspace
