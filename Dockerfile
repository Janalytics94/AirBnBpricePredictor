FROM python:3.8-slim-buster

WORKDIR /root/lib/

#COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

#RUN pip3 install -r requirements.txt 