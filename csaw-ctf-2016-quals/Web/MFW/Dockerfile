FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y apache2 php libapache2-mod-php git

RUN echo "Listen 8000" >> /etc/apache2/ports.conf
RUN echo "zend.assertions = 1" >> /etc/php/7.0/apache2/php.ini

COPY ./src /var/www/html

WORKDIR /var/www/html
RUN rm index.html
RUN git config --global user.email "git@github.com" && git config --global user.name "Github"
RUN git init && git add -A && git commit -m "I love PHP's typesafety!"

RUN echo '<?php $FLAG="flag{3vald_@ss3rt_1s_best_a$$ert}"; ?>' > templates/flag.php

CMD /usr/sbin/apache2ctl -D FOREGROUND
