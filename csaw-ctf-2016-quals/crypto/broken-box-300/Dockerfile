FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python

WORKDIR /opt/brokenbox

COPY ./broken_box.py ./

CMD ["python", "./broken_box.py"]
