FROM jjanzic/docker-python3-opencv

WORKDIR /root/

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git \
    apt-get install ffmpeg libsm6 libxext6  -y
#RUN pip3 install -r requirements.txt 