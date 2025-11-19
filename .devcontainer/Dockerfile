FROM mcr.microsoft.com/devcontainers/base:latest

USER root

RUN --mount=type=secret,id=mysecret,target=/tmp/foo_bar_credentials \
    ## You have access to the secret contents as a file, so you can read it
    export GITLAB_AUTH_TOKEN=$(cat /tmp/foo_bar_credentials) \
    && echo $GITLAB_AUTH_TOKEN > /abc
