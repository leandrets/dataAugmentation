# dataAugmentation

## Description
Simple Python application that extracts frames from a set of videos and applies data augmentation techniches on them.

## Running
1) Clone this repository with `git clone https://gitlab.com/activities1/backvisao.git`
2) Build the Dockerfile using `sudo docker build -t project .`
3) Run the Docker image with `sudo docker run -p 15672:15672 -p 5672:5672 rabbitmq:3.9.9-management-alpine` or any available port in your machine.