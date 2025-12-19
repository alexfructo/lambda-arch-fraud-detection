FROM confluentinc/cp-kafka:7.3.0

USER root

COPY init-kafka.sh /init-kafka.sh
RUN chmod +x /init-kafka.sh

ENTRYPOINT ["/init-kafka.sh"]
