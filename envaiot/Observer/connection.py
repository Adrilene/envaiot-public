from pyrabbit.api import Client


def get_bindings(host, user, password, exchange):
    client = Client(host, user, password)
    bindings = client.get_bindings()
    bindings_result = []

    for b in bindings:
        if b["source"] == exchange:
            bindings_result.append(b)

    return bindings_result


def subscribe_in_all_queues(host, user, password, exchange, queue, channel):
    bindings = get_bindings(
        host,
        user,
        password,
        exchange,
    )

    for bind in bindings:
        channel.queue_bind(
            exchange=bind["source"],
            queue=queue,
            routing_key=bind["routing_key"],
        )

    return bindings
