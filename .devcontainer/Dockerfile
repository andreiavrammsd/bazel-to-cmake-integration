FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    cmake \
    curl \
    g++ \
    gcc \
    gnupg \
    make \
    openjdk-17-jdk \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > /usr/share/keyrings/bazel-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list \
    && apt-get update && apt-get install -y bazel-7.6.1 \
    && ln -s /usr/bin/bazel-7.6.1 /usr/bin/bazel \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project
