FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y tesseract-ocr libtesseract3 npm nodejs

WORKDIR /opt/ivninja
COPY ./ /opt/ivninja

RUN mkdir -p uploads

RUN npm install express multer morgan express-rate-limit

CMD nodejs server.js
