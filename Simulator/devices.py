from flask import jsonify

from .communication_service import CommunicationService
from .publisher import DevicePublisher
from .subscriber import DeviceSubscriber
from .utils import write_log


class Device:
    def __init__(self, name, status, senders, exchange, host):
        self.name = name
        self.status = status
        self.current_status = self.status[0]
        self.publisher = DevicePublisher(exchange, name, host)
        self.subscriber = DeviceSubscriber(exchange, name, senders, host)

    def get_status(self):
        return {"status": self.current_status}

    def set_status(self, new_status):
        if new_status in self.status:
            write_log(
                f"{self.name} changed status from {self.current_status} to {new_status}."
            )
            self.current_status = new_status
            return {"received": new_status, "new status": self.current_status}

        return {"error": "Inexistent Status"}

    def create_queue_and_routes(self, exchange, host):
        CommunicationService(exchange, host)
