FROM ubuntu:16.04

RUN dpkg --add-architecture i386
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libc6:i386

WORKDIR /home/spaghetti

# Create users
RUN adduser --disabled-password --gecos '' spaghetti

# setup flag
COPY ./moms_spaghetti/moms_spaghetti /home/spaghetti/
RUN chown -R root:root /home/spaghetti
RUN chmod 750 /home/spaghetti
COPY ./flag.txt /home/spaghetti/
RUN chown root:spaghetti /home/spaghetti/flag.txt
RUN chmod 440 /home/spaghetti/flag.txt

RUN chown spaghetti /home/spaghetti
RUN chmod 500 /home/spaghetti
RUN chown spaghetti:spaghetti /home/spaghetti/moms_spaghetti
RUN chmod 750 /home/spaghetti/moms_spaghetti


CMD su "spaghetti" -c "/home/spaghetti/moms_spaghetti"
