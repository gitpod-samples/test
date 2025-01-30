FROM gitpod/workspace-base

USER root

RUN <<'END_OF_RUN'

# Install necessary dependencies
apt-get update && apt install xdg-utils netcat --no-install-recommends -yq

# Set /.supervisor/browser.sh as the default browser
cat > /usr/share/applications/supervisor-browser.desktop << DESKTOP
[Desktop Entry]
Version=1.0
Name=Supervisor Browser
Comment=Browser handler for supervisor environment
Exec=/.supervisor/browser.sh %u
Terminal=false
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/vnd.mozilla.xul+xml;application/rss+xml;application/rdf+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;
DESKTOP
xdg-settings set default-web-browser supervisor-browser.desktop

# Modify logic of /.supervisor/browser.sh when the workspace starts
cat >> /etc/bash.bashrc <<'BASH'

if mkdir /tmp/.custom_browser.lock 2>/dev/null && test -e /.supervisor/browser.sh; then
  cat > /.supervisor/browser.sh <<'BROWSER'
#!/bin/bash

url="$@"
if [[ "$url" =~ ^file:// ]]; then
        for port in {1234..2000}; do
                (echo >/dev/tcp/localhost/${port}) 2>/dev/null && continue
                url="http://localhost:${port}"
                { printf 'HTTP/1.0 200 OK\r\n\r\n'; cat "${url#file://}"; } | nc -l -p $port -q 1 & break
        done
fi

gp preview --external "$url"
BROWSER
fi

BASH

END_OF_RUN


