FROM ubuntu:20.04
RUN sudo apt-get install git python3 python3-opencv
RUN pip3 install numpy
RUN git clone https://gitlab.com/activities1/backvisao.git
RUN cd backvisao
RUN python3 main.py > output.log