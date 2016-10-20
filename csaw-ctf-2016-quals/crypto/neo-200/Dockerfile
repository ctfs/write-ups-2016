FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl
RUN adduser --disabled-password --gecos '' neo

# no tty
ENV DEBIAN_FRONTEND noninteractive

# global installs [applies to all envs!]
RUN apt-get install -y build-essential git python3 python3-dev python3-setuptools python3-pip python-virtualenv

# create a virtual environment and install all depsendecies from pypi
RUN virtualenv -p python3 /opt/venv
ADD ./requirements.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip install -r /opt/venv/requirements.txt

COPY ./app/ /opt/venv/app/
COPY ./gunicorn_config.py /opt/venv/gunicorn_config.py
RUN chown -R root:neo /opt/venv/

WORKDIR /opt/venv/
CMD . /opt/venv/bin/activate && gunicorn --config gunicorn_config.py app:create_app\(\)
