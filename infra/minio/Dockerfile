FROM minio/mc

USER root

# Copia script
COPY init-minio.sh /init-minio.sh

# Copia modelos seed para dentro do container
COPY seed /seed

RUN chmod +x /init-minio.sh

ENTRYPOINT ["/init-minio.sh"]
