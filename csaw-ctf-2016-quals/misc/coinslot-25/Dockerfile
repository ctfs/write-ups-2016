FROM ubuntu:16.04
MAINTAINER Little Example "little@example.com"
LABEL Description="CSAW 2016 Little Example" VERSION=1.0

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat python3

#user
RUN adduser --disabled-password --gecos '' noobie
RUN chown -R root:noobie /home/noobie/
RUN chmod 750 /home/noobie
RUN touch /home/noobie/flag.txt
RUN chown root:noobie /home/noobie/flag.txt
RUN chmod 440 /home/noobie/flag.txt
WORKDIR /home/noobie/

COPY ./coins.py /home/noobie
COPY ./flag.txt /home/noobie

CMD socat TCP-LISTEN:8000,reuseaddr,fork EXEC:"python3 /home/noobie/coins.py"
