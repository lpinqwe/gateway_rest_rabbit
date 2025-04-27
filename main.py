import os
import uuid
import json
import pika
import threading
from flask import Flask

payload = None
app = Flask(__name__)

from utils.RabbitRabbit import RabbitRabbit

# Создаем глобальную переменную для ожидания результата
response_event = threading.Event()
response_data = None

@app.route('/')
def home():
    return "Hello, World!"






@app.route('/data/json', methods=['GET'])
def getJSONtest():
    global response_data
    unique_id = str(uuid.uuid4())

    message = {
        "msgCommand": "getjson",
        "msgID": unique_id,
        "msgPayload": ""
    }
    properties = pika.BasicProperties(expiration='60000')
    credentials = pika.PlainCredentials(username=os.getenv('RABBITMQ_USER'.upper(), 'guest'),
                                         password=os.getenv('RABBITMQ_pass'.upper(), 'guest'))

    connection_param = pika.ConnectionParameters(host=os.getenv('rabbit_localhost'.upper(), '127.0.0.1'),
                                                 port=os.getenv('rabbit_port'.upper(), 5672),
                                                 credentials=credentials
                                                 )

    connection = pika.BlockingConnection(connection_param)

    channel = connection.channel()

    # Подключение к RabbitMQ
    channel.queue_declare(queue=unique_id)

    # Отправка сообщения
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('rabbitQue2'.upper(), 'getQ2'),
        body=json.dumps(message).encode('utf-8')
    )

    # Вместо basic_get, используем basic_consume
    # создадим функцию для асинхронного получения сообщений

    def consume_message(ch, method, properties, body):
        global response_data
        try:
            response = json.loads(body)
            response_data = response  # Сохраняем данные в глобальную переменную
            print(f"Received payload: {response_data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            response_event.set()  # Устанавливаем флаг, что данные получены
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    # Запуск потребителя в отдельном потоке, чтобы не блокировать выполнение
    def start_consuming():
        channel.basic_consume(queue=unique_id, on_message_callback=consume_message, auto_ack=False)
        channel.start_consuming()

    consumer_thread = threading.Thread(target=start_consuming)
    consumer_thread.daemon = True
    consumer_thread.start()

    # Ожидаем, пока не получим данные
    response_event.wait()

    # Вернем результат клиенту
    if response_data:
        return json.dumps(response_data)
    else:
        return "No response received."

@app.route('/data/xml', methods=['GET'])
def getXMLtest():
    global response_data
    unique_id = str(uuid.uuid4())

    message = {
        "msgCommand": "getxml",
        "msgID": unique_id,
        "msgPayload": ""
    }
    properties = pika.BasicProperties(expiration='60000')
    credentials = pika.PlainCredentials(username=os.getenv('RABBITMQ_USER'.upper(), 'guest'),
                                         password=os.getenv('RABBITMQ_pass'.upper(), 'guest'))

    connection_param = pika.ConnectionParameters(host=os.getenv('rabbit_localhost'.upper(), '127.0.0.1'),
                                                 port=os.getenv('rabbit_port'.upper(), 5672),
                                                 credentials=credentials
                                                 )

    connection = pika.BlockingConnection(connection_param)

    channel = connection.channel()

    # Подключение к RabbitMQ
    channel.queue_declare(queue=unique_id)

    # Отправка сообщения
    channel.basic_publish(
        exchange='',
        routing_key=os.getenv('rabbitQue2'.upper(), 'getQ2'),
        body=json.dumps(message).encode('utf-8')
    )

    # Вместо basic_get, используем basic_consume
    # создадим функцию для асинхронного получения сообщений

    def consume_message(ch, method, properties, body):
        global response_data
        try:
            response = json.loads(body)
            response_data = response  # Сохраняем данные в глобальную переменную
            print(f"Received payload: {response_data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            response_event.set()  # Устанавливаем флаг, что данные получены
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    # Запуск потребителя в отдельном потоке, чтобы не блокировать выполнение
    def start_consuming():
        channel.basic_consume(queue=unique_id, on_message_callback=consume_message, auto_ack=False)
        channel.start_consuming()

    consumer_thread = threading.Thread(target=start_consuming)
    consumer_thread.daemon = True
    consumer_thread.start()

    # Ожидаем, пока не получим данные
    response_event.wait()

    # Вернем результат клиенту
    if response_data:
        return json.dumps(response_data)
    else:
        return "No response received."



if __name__ == '__main__':
    app.run(debug=True)
