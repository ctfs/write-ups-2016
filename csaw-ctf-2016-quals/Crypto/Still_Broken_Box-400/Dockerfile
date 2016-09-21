FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python

WORKDIR /opt/stillbrokenbox

COPY ./still_broken_box.py ./

CMD ["python", "./still_broken_box.py"]
