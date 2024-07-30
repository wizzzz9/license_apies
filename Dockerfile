FROM ubuntu:latest
LABEL authors="aker"

ENTRYPOINT ["top", "-b"]