FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty
ENV DEBIAN_FRONTEND noninteractive

# global installs [applies to all envs!]
RUN apt-get install -y python python-pip python-dev
RUN pip install Twisted


WORKDIR /opt/sleeping/
COPY ./sleeping.py /opt/sleeping/
COPY ./sleeping.png /opt/sleeping/

EXPOSE 8000
CMD ["python", "./sleeping.py"]
