FROM ubuntu:14.04

# dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc

WORKDIR /opt/wtf.sh

# Create users
# web user -- everything will run under this one
RUN adduser --disabled-password --gecos '' www
# flag1 user -- flag1 will be owned by this, read_flag1 will setuid to be this
RUN adduser --disabled-password --gecos '' flag1
# flag2 user -- flag2 will be owned by this, read_flag2 will setuid to be this
RUN adduser --disabled-password --gecos '' flag2


# setup flags
COPY ./data/flag1.txt /home/flag1/
COPY ./data/flag2.txt /home/flag2/
RUN chown -R root:root /home/flag1/
RUN chown -R root:root /home/flag2/
RUN chown root:flag1 /home/flag1/flag1.txt
RUN chown root:flag2 /home/flag2/flag2.txt

RUN chmod 440 /home/flag1/flag1.txt
RUN chmod 440 /home/flag2/flag2.txt

# setgid programs to read flags
COPY ./get_flag1.c /tmp/
COPY ./get_flag2.c /tmp/
RUN gcc /tmp/get_flag1.c -o /usr/bin/get_flag1
RUN gcc /tmp/get_flag2.c -o /usr/bin/get_flag2
RUN chown root:flag1 /usr/bin/get_flag1
RUN chown root:flag2 /usr/bin/get_flag2

RUN chmod 2755 /usr/bin/get_flag1
RUN chmod 2755 /usr/bin/get_flag2


# assorted permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm
# TODO: Resource limits


# setup webapp
COPY ./src /opt/wtf.sh
COPY ./spinup.sh /opt/wtf.sh

COPY ./data/ /tmp/data/

RUN chown -R www /opt/wtf.sh
RUN chmod -R 555 /opt/wtf.sh

RUN /tmp/data/setup_data.sh
RUN chmod -R 777 /opt/wtf.sh/posts
RUN chmod -R 777 /opt/wtf.sh/users
RUN chmod -R 777 /opt/wtf.sh/users_lookup

RUN echo "tmpfs    /tmp/wtf_runtime    tmpfs    nodev,nosuid,size=1G    0    0" >> /etc/fstab


# clear out /tmp/data, as it might contain flags (it should be cleaned at boot, but better safe than sorry)
CMD rm -rf /tmp/data

WORKDIR /tmp/wtf_runtime/wtf.sh
EXPOSE 8000
CMD /opt/wtf.sh/spinup.sh
