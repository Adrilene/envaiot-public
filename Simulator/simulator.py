from flask import jsonify

from .devices import Device
from .utils import get_current_device, get_exchange_name, write_log


class Simulator:
    def __init__(self):
        self.devices = []

    def configure(self, configuration):
        self.devices = []
        exchange_name = get_exchange_name(configuration["project"])
        for device in configuration["resources"].keys():
            status = configuration["resources"][device]["status"] + [
                "active",
                "inactive",
            ]
            senders = configuration["resources"][device]["senders"]
            host = configuration["communication"]["host"]
            self.devices.append(Device(device, status, senders, exchange_name, host))

        for device in self.devices:
            device.subscriber.start()

        return jsonify(
            {"Devices instatiated": [device.name for device in self.devices]}
        )

    def get_devices_list(self):
        return jsonify(
            {
                "Devices instatiated": [
                    f"{device.name} - {device.current_status}"
                    for device in self.devices
                ]
            }
        )

    def status(self, device_name, new_status=None):
        current_device = get_current_device(device_name, self.devices)

        if not current_device:
            msg = f"From request to change status: Device Not Found {device_name}"
            write_log(msg)
            return {"error": msg}

        if not new_status:
            return current_device.get_status()

        if new_status not in current_device.status:
            msg = f"From request to change status: Status not available for device {device_name}"
            write_log(msg)
            return {"error": msg}

        return current_device.set_status(new_status)

    def send_message(self, device_name, message):
        current_device = get_current_device(device_name, self.devices)
        if "to" in message.keys():
            recipient_device = get_current_device(message["to"], self.devices)
            if not recipient_device:
                msg = f"Device Not Found {device_name}"
                write_log(msg)
                return {"error": msg}

        if not current_device:
            msg = f"Device Not Found {device_name}"
            write_log(msg)
            return {"error": msg}

        new_message = {"type": message["type"], "body": message["body"]}
        if not "to" in message.keys():
            write_log(f"{device_name} published {new_message}")
        else:
            write_log(f"{device_name} sent {new_message} to {message['to']}.")

        return {
            "success": current_device.publisher.publish(
                new_message,
                device_name=device_name,
                recipient=message["to"] if "to" in message.keys() else None,
            )
        }
