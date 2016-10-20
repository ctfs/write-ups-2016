FROM ubuntu:14.04
MAINTAINER unknonwn
LABEL Description="CSAW 2016 Tutorial" VERSION='1.0'

#installation
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y build-essential

#user
RUN adduser --disabled-password --gecos '' tutorial
RUN chown -R root:tutorial /home/tutorial/
RUN chmod 750 /home/tutorial
RUN touch /home/tutorial/flag.txt
RUN chown root:tutorial /home/tutorial/flag.txt
RUN chmod 440 /home/tutorial/flag.txt
RUN chmod 740 /usr/bin/top
RUN chmod 740 /bin/ps
RUN chmod 740 /usr/bin/pgrep
RUN export TERM=xterm

WORKDIR /home/tutorial/
COPY tutorial.c /home/tutorial
COPY flag.txt /home/tutorial

RUN gcc -Wall -o tutorial tutorial.c -ldl 

CMD ["/home/tutorial/tutorial","4242"]

