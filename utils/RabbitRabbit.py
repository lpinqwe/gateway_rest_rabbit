import os
import os
import threading

import pika

import decor.singletone
#import main
from interfaces.CommandStructure import Command
from utils.Factory import Factory


@decor.singletone.singleton
class RabbitRabbit:

    def __init__(self):

        self.properties = pika.BasicProperties(expiration='60000')
        self.credentials = pika.PlainCredentials(username=os.getenv('RABBITMQ_USER'.upper(), 'guest'),
                                                 password=os.getenv('RABBITMQ_pass'.upper(), 'guest'))

        self.connection_param = pika.ConnectionParameters(host=os.getenv('rabbit_localhost'.upper(), '127.0.0.1'),
                                                          port=os.getenv('rabbit_port'.upper(), 5672),
                                                          credentials=self.credentials
                                                          )

        self.connection = pika.BlockingConnection(self.connection_param)

        self.channel = self.connection.channel()

        self.publishQue = os.getenv('rabbitQue2'.upper(), 'getQ2')
        self.watcherQue = os.getenv('rabbitQue1'.upper(), 'getQ1')
        self.channel.queue_declare(queue=self.publishQue)
        self.channel.queue_declare(queue=self.watcherQue)

        self.channel.basic_consume(queue=self.watcherQue, on_message_callback=self.callback, auto_ack=False)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        try:
            tmp = body.decode()

            tmp = Command(tmp)

            #main.payload = Command.msgPayload

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            tmp = body.decode()

            tmp = Command(tmp)
            print(e)
            print(tmp)

    def sendMessage(self, msg: Command):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publishQue,
            body=msg.get(),
            mandatory=True
        )

    def start_consuming(self):
        # можно добавить список для увеличения кол-ва потоков
        # или просто запуск нескольких сервисов
        self.consumerThread = threading.Thread(target=self.receive_messages)
        self.consumerThread.daemon = True
        self.consumerThread.start()
