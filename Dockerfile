FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get -y install python3 python3-pip
RUN pip3 install numpy 
RUN apt-get -y install ffmpeg python3-opencv

WORKDIR /usr/app/src

COPY . .

WORKDIR /usr/app/src/src

CMD python3 main.py > ../output/output.log

EXPOSE 5672