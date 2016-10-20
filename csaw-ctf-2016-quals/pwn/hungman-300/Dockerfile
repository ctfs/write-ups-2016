FROM ubuntu:16.04
MAINTAINER unknonwn
LABEL Description="CSAW 2016 Hungman" VERSION='1.0'

#installation
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential socat

#user
RUN adduser --disabled-password --gecos '' hungman
RUN chown -R root:hungman /home/hungman/
RUN chmod 750 /home/hungman
RUN touch /home/hungman/flag.txt
RUN chown root:hungman /home/hungman/flag.txt
RUN chmod 440 /home/hungman/flag.txt
RUN export TERM=xterm

WORKDIR /home/hungman/
COPY hungman /home/hungman
COPY flag.txt /home/hungman

EXPOSE 8000
CMD su hungman -c "socat -T10 TCP-LISTEN:8000,reuseaddr,fork EXEC:/home/hungman/hungman"
