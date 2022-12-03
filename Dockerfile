# Docker file for metadata_burn ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-metadata-burn .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-metadata-burn .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-metadata-burn
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-metadata-burn
#

FROM python:3.9.1-slim-buster
LABEL maintainer="John Pastore <dev@babyMRI.org>"

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y fontconfig && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install .

CMD ["metadata_burn", "--help"]
