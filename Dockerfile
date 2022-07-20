FROM python:3

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install numpy 
RUN apt-get -y install ffmpeg python3-opencv

COPY . .

WORKDIR /src

CMD python3 main.py > ../output/output.log

EXPOSE 5672