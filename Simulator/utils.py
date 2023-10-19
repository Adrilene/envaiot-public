import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
import sys

sys.path.append("..")


def write_log(message):
    with open(f"{os.getenv('LOGS_PATH')}", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {message}\n")


def get_exchange_name(project_name):
    return f"{project_name.lower().replace(' ', '_')}_exchange"


def get_current_device(device_name, devices_list):
    current_device = None
    for device in devices_list:
        if device.name == device_name:
            current_device = device
    return current_device


def get_publishing_routing_key(device_name):
    alias = "".join([c for c in device_name if c.isupper()]).lower()

    return f"{alias}_info"


def get_subscribing_routing_key(device_name):
    alias = "".join([c for c in device_name if c.isupper()]).lower()

    return f"{alias}_msg"


def get_queue_name(device_name):
    return f"queue_{device_name.lower()}"


def get_exchange_name(project_name):
    return f"{project_name.lower().replace(' ', '_')}_exchange"
