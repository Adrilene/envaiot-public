import json

import pika

from .communication_service import CommunicationService
from .utils import get_publishing_routing_key, get_subscribing_routing_key


class DevicePublisher(CommunicationService):
    def __init__(self, exchange, device_name):
        CommunicationService.__init__(self, exchange)
        self.routing_key = get_publishing_routing_key(device_name)

    def publish(self, message, device_name, recipient):
        rk = self.routing_key

        if recipient:
            rk = get_subscribing_routing_key(recipient)

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=rk,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
            body=json.dumps(message),
        )

        print(f"PUBLISH {device_name} | {message} | {rk}")
        return f"{device_name} published in {rk}"
