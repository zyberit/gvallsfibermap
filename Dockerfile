FROM grahamdumpleton/mod-wsgi-docker:python-3.5-onbuild

VOLUME /app/db

EXPOSE 80
CMD [ "--access-log", "--log-to-terminal", "--url-alias", "/static", "static", "config/wsgi.py" ]
#EXPOSE 443
#CMD [ "--https-port", "443", "--url-alias", "/static", "static", "--server-name", "dagliga-slagningar.apps.violaberg.nu", "--ssl-certificate-file", "/app/keys/cert.cer", "--ssl-certificate-key-file", "/app/keys/key.key", "--ssl-certificate-chain-file", "/app/keys/chain.cer", "--log-level", "warn", "--access-log", "--log-to-terminal", "--startup-log", "config/wsgi.py" ]
