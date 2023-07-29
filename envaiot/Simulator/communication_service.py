import pika
import os


class CommunicationService:
    def __init__(self, exchange):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = connection.channel()
        self.exchange = exchange
        self.declare_exchange(exchange)

    def declare_exchange(self, exchange):
        self.channel.exchange_declare(exchange=exchange, exchange_type="topic")

    def declare_queue(self, queue):
        self.channel.queue_declare(queue, durable=False)

    def bind_exchange_queue(self, exchange, queue, routing_key):
        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key,
        )
