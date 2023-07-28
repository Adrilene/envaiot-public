from flask import jsonify

from .devices import Device
from .string_operations import get_exchange_name
from .utils import get_current_device, write_log


class Simulator:
    def __init__(self):
        self.devices = []

    def configure(self, resources, project):
        self.devices = []
        exchange_name = get_exchange_name(project)
        for device in resources.keys():
            status = resources[device]["status"] + ["active", "inactive"]
            senders = resources[device]["senders"]
            self.devices.append(Device(device, status, senders, exchange_name))

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
            write_log(f"From request to change status: Device Not Found {device_name}")
            return jsonify({"Error": f"Device Not Found {device_name}"}), 400

        if not new_status:
            return current_device.get_status()

        if new_status not in current_device.status:
            write_log(
                f"From request to change status: Status not available for device {device_name}"
            )
            return jsonify(f"Status not available for device {current_device}"), 400

        return current_device.set_status(new_status)

    def send_message(self, device_name, message):
        current_device = get_current_device(device_name, self.devices)

        if not current_device:
            return {"Error": f"Device Not Found {device_name}"}

        recipient_device = message.pop("to") if "to" in message.keys() else None

        if recipient_device:
            recipient_device = get_current_device(message["to"], devices)
            if not recipient_device:
                return {"Error": f"Device Not Found {device_name}"}
            write_log(f"{device_name} sent {message} to {recipient_device}.")

        else:
            write_log(f"{device_name} published {message}")

        return {
            "Success": current_device.publisher.publish(
                message, device_name=device_name, recipient=recipient_device
            )
        }
