FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

USER root

RUN --mount=type=secret,id=mysecret,target=/tmp/lol cat /tmp/lol > /abc


# use this Dockerfile to install additional tools you might need, e.g.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
