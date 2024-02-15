FROM ubuntu:latest
ARG USER=user
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install -y \
    sudo\
    make\
    git

RUN useradd -m $USER && echo "$USER:$USER" | chpasswd && adduser $USER sudo
RUN echo "user            ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers
CMD /bin/bash