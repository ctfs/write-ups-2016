FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc socat libreadline-dev make

# create users
RUN adduser --disabled-password -gecos '' lua

# build
WORKDIR /tmp/
COPY ./ /tmp/
RUN chmod +x ./build.sh
RUN ./build.sh

# copy built files
RUN mkdir -p /opt/lua/ && cp ./run.sh ./scripty ./server.lua ./server.luac ./flag /opt/lua/

# permissions
RUN chown -R root:lua /opt/lua/
RUN chmod 750 /opt/lua/
RUN chmod 440 /opt/lua/flag

WORKDIR /opt/lua/
EXPOSE 8000
CMD su lua -c "/opt/lua/run.sh"
