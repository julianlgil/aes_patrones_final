import json
import os
import time

import pika


class RabbitMQ:
    def __init__(self, amqp_url) -> None:
        url_params = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(url_params)
        self.chan = self.connection.channel()

    def publish(self, queue, message) -> None:
        self.chan.queue_declare(queue=queue, durable=True)
        self.chan.basic_publish(
            exchange="",
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def subscribe(self, queue, callback) -> None:
        self.chan.queue_declare(queue=queue, durable=True)
        self.chan.basic_qos(prefetch_count=1)
        self.chan.basic_consume(queue=queue, on_message_callback=callback)
        print("Waiting to consume ", queue)
        self.chan.start_consuming()

    def close_connection(self) -> None:
        self.chan.close()
        self.connection.close()


class RabbitCallback:
    def __init__(self, rabbit: RabbitMQ) -> None:
        self.rabbit = rabbit

    def get_message(self, ch, method, properties, body):
        try:
            source = body.decode("utf-8")
            source = json.loads(source)
            time.sleep(2)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("** ** ** source ** ** **", source)

        except Exception as e:
            print(f"Error con el filtro: {e}")


def send_rabbit_message(message: dict):
    # Publicar mensaje en la cola
    rabbit = RabbitMQ(amqp_url=os.environ["AMQP_URL"])
    if isinstance(message, dict):
        message_str = {key: str(value) for key, value in message.items()}
        message_str = json.dumps(message_str)
    elif isinstance(message, str):
        message_str = message
    else:
        message_str = str(message)
    queue_to_process_payments = os.getenv("QUEUE_TO_PROCESS_PAYMENTS")
    rabbit.publish(queue_to_process_payments, message_str)
    rabbit.close_connection()


async def subscribe_queue():
    rabbit = RabbitMQ(amqp_url=os.environ["AMQP_URL"])
    source_queue = os.getenv("QUEUE_TO_PROCESS_PAYMENTS")
    rabbit.subscribe(source_queue, RabbitCallback(rabbit).get_message)


"""

Para suscribirse a una cola
rabbit = RabbitMQ(amqp_url=os.environ["AMQP_URL"])
source_queue = os.getenv("QUEUE_TO_PROCESS_PAYMENTS")
rabbit.subscribe(source_queue, RabbitCallback(rabbit).get_message)

Para publicar a una cola
rabbit = RabbitMQ(amqp_url=os.environ["AMQP_URL"])
message_to_send = ""
rabbit.publish(source_queue, json.dumps(message_to_send))
rabbit.close_connection()

"""
