FROM python:3.8-slim-buster

WORKDIR root/

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt 