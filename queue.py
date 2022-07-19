import pika
import json
from extractor import Extractor

class JSONdataSender:
    
    # Sets connection and channel
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

    # Reads data from JSON file and stores it, returns amount of messages in the file
    def setData(self, path):
        file =  open(path, 'r')
        self.data = json.load(file)
        return len(self.data)
        
    # Sends stored data to queue
    def sendData(self, queueName):
        self.channel.queue_declare(queue=queueName)
        for item in self.data:
            self.channel.basic_publish(exchange='',
                            routing_key=queueName,
                            body=str(item))
        self.connection.close()
        

class Consumer:
    counter = 0
    
    #  Sets connection and channel
    def __init__(self, name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.queueName = name
        
    # Called everytime a message is received - redirects body of message to frame extractor
    def callback(self, ch, method, properties, body):
        print(f"\n-----------------------------------------------------\n{self.counter}: Received ", body)
        self.counter += 1
        self.extractor.extract(body)
        
    # Starts consumation of messages
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
        
    # Stops consumation of messages
    def stopConsumation(self):
        self.channel.stop_consuming()
        self.connection.close()
        print("\n\n-----------------------------------------------------\nTotal items received: ", self.counter)
        
    # Builds connection with a frame extractor
    def connect(self, extr):
        self.extractor = extr
    
