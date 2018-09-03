FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y wget curl sudo git libcurl4-openssl-dev ca-certificates build-essential python3 python3-pip \
    && apt-get install -y python python-dev python-pip \
    && pip3 install --upgrade pip \
    && useradd -m repl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN echo hey && git clone -b dev-comms https://github.com/datacamp/oil.git \
    && cd oil && pip2 install -e .

