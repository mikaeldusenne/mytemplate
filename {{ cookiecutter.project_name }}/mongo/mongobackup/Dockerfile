FROM mongo:bionic


RUN apt-get update && \
    apt-get install -y cron

ADD backup.sh /backup.sh
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chmod +x /backup.sh


ENTRYPOINT ["/entrypoint.sh"]
CMD [""]
