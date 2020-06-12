import abc
import logging
import os
import time

import pika
from pika.exceptions import AMQPConnectionError


class RabbitMQImpl:
    def __init__(self):
        RABBITMQ_URL = os.environ.get(
            "RABBITMQ_URL", "amqp://user:password@localhost:5672/%2F"
        )
        logging.debug(RABBITMQ_URL)

        self.connection = None
        while not self.connection:
            try:
                self.connection = pika.BlockingConnection(
                    pika.URLParameters(RABBITMQ_URL)
                )
                self.channel = self.connection.channel()
                logging.info("rabbitmq connected")
            except AMQPConnectionError:
                logging.error("waiting for RabbitMQ to become available...")
                time.sleep(3)

        self.channel.queue_declare(queue="start_hand_queue", durable=True)

    def publish(self, message):
        self.channel.exchange_declare(
            exchange="start_hand_queue", exchange_type="fanout"
        )
        self.channel.basic_publish(
            exchange="start_hand_queue",
            routing_key="start_hand_queue",
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2, content_type="application/json"
            )
            # todo: make message persistent or no?
        )
        print(f" [x] Sent {message}")

    def close(self):
        self.connection.close()
