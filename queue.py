import pika
import json
from extractor import Extractor

class JSONdataSender:
    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port="5672",
                credentials=credentials
            )
        )   
        self.channel = self.connection.channel()

    def setData(self, path):
        file =  open(path, 'r')
        self.data = json.load(file)
        return len(self.data)
        
    def sendData(self, queueName):
        self.channel.queue_declare(queue=queueName)
        for item in self.data:
            self.channel.basic_publish(exchange='',
                            routing_key=queueName,
                            body=str(item))
        self.connection.close()
        

class Receiver:
    counter = 0
    
    def __init__(self, name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.queueName = name
        
    def callback(self, ch, method, properties, body):
        #print("Received ", body)
        self.counter += 1
        self.extractor.extract(body)
        
    def startConsumation(self):
        self.channel.queue_declare(queue=self.queueName)
        self.channel.basic_consume(queue=self.queueName,
                      auto_ack=True,
                      on_message_callback=self.callback) 
        print(' [*] Waiting for messages. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.stopConsumation()
        
    def stopConsumation(self):
        self.channel.stop_consuming()
        self.connection.close()
        print("Total items received: ", self.counter)
        
    def connect(self, extr):
        self.extractor = extr
    

class CustomException(Exception):
    pass

sender = JSONdataSender()
quantity = sender.setData("ref/payload.json")
sender.sendData("messageQueue")

extr = Extractor()

receiver = Receiver("messageQueue")
receiver.connect(extr)
receiver.startConsumation()
