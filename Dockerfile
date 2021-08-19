FROM jjanzic/docker-python3-opencv

WORKDIR /root/airbnb/
COPY requirements.txt /root/airbnb/requirements.txt

RUN apt-get update && \
    apt-get install -y git &&\
    apt-get upgrade -y && \
    apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 -q install pip --upgrade
RUN pip3 install -r requirements.txt 
RUN pip3 install jupyter

RUN python -m spacy download en_core_web_sm 
#CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]