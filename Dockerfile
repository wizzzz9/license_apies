FROM python:3.10.9-slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/requirements_dev.txt

COPY . .

RUN chmod a+x docker/*.sh