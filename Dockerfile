FROM jjanzic/docker-python3-opencv

WORKDIR /root/

COPY requirements.txt /root/requirements.txt

RUN apt-get update && \
    apt-get install -y git &&\
    apt-get upgrade -y && \
    apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install -r requirements.txt 

RUN python -m spacy download en_core_web_sm 