FROM python:3.8-slim-buster
#FROM dvcorg/cml:latest
#WORKDIR /root/

#COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

#RUN pip3 install -r requirements.txt 