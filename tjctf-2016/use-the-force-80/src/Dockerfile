FROM ubuntu
RUN apt-get -q -y update
RUN apt-get -q -y install python3 python3-pip sudo
RUN pip3 install Flask gunicorn
RUN useradd -m app
WORKDIR /home/app
CMD sudo -u app /usr/local/bin/gunicorn -b 0.0.0.0:5000 -w 4 app:app
ADD ./ /home/app/
RUN chmod -R ugo-w /home/app
