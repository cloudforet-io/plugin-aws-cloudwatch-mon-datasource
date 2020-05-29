FROM python:3

ENV PYTHONUNBUFFERED 1
ENV SPACEONE_PORT 50051
ENV SERVER_TYPE grpc
ENV PKG_DIR /tmp/pkg
ENV SRC_DIR /tmp/src

COPY src ${SRC_DIR}
ARG CACHEBUST=1
WORKDIR ${SRC_DIR}
RUN python3 setup.py install && \
    rm -rf /tmp/*

EXPOSE ${SPACEONE_PORT}

ENTRYPOINT ["spaceone"]
CMD ["grpc", "monitoring"]
