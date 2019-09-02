FROM raspbian/jessie

RUN apt-get update -y
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget -y
RUN apt-get install vim -y
RUN apt-get install git -y
RUN apt-get install curl -y

WORKDIR /tmp

RUN curl -O https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz

RUN tar -xf Python-3.7.4.tar.xz
WORKDIR /tmp/Python-3.7.4
RUN ./configure

RUN make -j 8
RUN make install
