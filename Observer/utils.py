import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


def get_sender_routing_key(device_name):
    alias = "".join([c for c in device_name if c.isupper()]).lower()

    return f"{alias}_info"


def get_receiver_routing_key(device_name):
    alias = "".join([c for c in device_name if c.isupper()]).lower()

    return f"{alias}_msg"


def get_exchange_name(project_name):
    return f"{project_name.lower().replace(' ', '_')}_exchange"


def get_scenario(received_message, received_topic):
    scenario = received_message
    scenario["topic"] = received_topic
    return scenario


def write_log(message):
    with open(f"../{os.getenv('LOGS_PATH')}", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {message}\n")
