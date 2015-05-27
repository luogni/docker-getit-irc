FROM ubuntu:14.04
MAINTAINER Luca Ognibene, luca.ognibene@gmail.com

RUN apt-get update && \
    apt-get upgrade -y

RUN apt-get -y install \
    weechat \
    weechat-scripts

RUN adduser --disabled-login --gecos '' weechat
COPY "wdl.py" "/home/weechat/wdl.py"

USER weechat
WORKDIR /home/weechat

VOLUME ["/media"]

ENTRYPOINT ["/usr/bin/weechat"]
