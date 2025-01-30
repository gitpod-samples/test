FROM gitpod/workspace-base

USER root

RUN <<'END_OF_RUN'

apt-get update && apt install netcat --no-install-recommends -yq

xdg_open=/usr/bin/xdg-open
cat > "${xdg_open}" <<'BROWSER'
#!/bin/bash

url="$@"
if [[ "$url" =~ ^file:// ]]; then
        for port in {1234..2000}; do
                (echo >/dev/tcp/localhost/${port}) 2>/dev/null && continue
                { printf 'HTTP/1.0 200 OK\r\n\r\n'; cat "${url#file://}"; } | nc -l -p $port -q 1 &
                url="http://localhost:${port}"
                break
        done
fi

gp preview --external "$url"
BROWSER

sudo chmod +x "${xdg_open}"

END_OF_RUN


