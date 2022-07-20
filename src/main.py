from queue import JSONdataSender
from queue import Consumer
from extraction import Extractor
from imageproc import Operator



sender = JSONdataSender()
quantity = sender.setData("../ref/payload.json")
sender.sendData("messageQueue")

extr = Extractor()
opr = Operator()
extr.connect(opr)

consumer = Consumer("messageQueue")
consumer.connect(extr)
consumer.startConsumation()
