# base image
FROM ubuntu:18.04

# ubuntu installing - python, pip
RUN apt-get update &&\
    apt-get install python3.6 -y &&\
    apt-get install python3-pip -y

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /streamlit-docker

# copy over requirements
COPY /docker/requirements.txt ./tmp/requirements.txt

# install pip then packages
RUN pip3 install -r ./tmp/requirements.txt

# copying all files over
COPY ./web ./web
COPY ./data ./data

# streamlit-specific commands
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# cmd to launch app when container is run
CMD streamlit run ./web/st_without_postgres.py  --server.enableWebsocketCompression=false
