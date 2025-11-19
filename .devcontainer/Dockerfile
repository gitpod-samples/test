FROM mcr.microsoft.com/devcontainers/base:latest

RUN --mount=type=secret,id=mysecret,target=/tmp/foo_bar_credentials \
    ## You have access to the secret contents as a file, so you can read it, don't run the cat command in production!
    # cat /tmp/foo_bar_credentials \
    ## or use it as an environment variable
    export GITLAB_AUTH_TOKEN=$(cat /tmp/foo_bar_credentials) && \
    ## Use the secret in your commands, e.g., to authenticate with a package repository
    /opt/conda/bin/pip install 'dsutils' --index-url https://__token__:$GITLAB_AUTH_TOKEN@gitlab.com/api/v4/projects/43262283/packages/pypi/simple
