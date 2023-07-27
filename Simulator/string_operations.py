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
