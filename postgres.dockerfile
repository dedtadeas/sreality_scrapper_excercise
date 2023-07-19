FROM postgres:15.1-alpine

LABEL author="TadeasDed"
LABEL description="Postgres Image for Luxonis demo"
LABEL version="1.0"

COPY postgres-init/*.sql /docker-entrypoint-initdb.d/