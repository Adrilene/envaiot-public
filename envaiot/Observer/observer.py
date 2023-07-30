import json
from copy import deepcopy
from threading import Thread
from termcolor import colored

from .communication_service import CommunicationService
from .connection import subscribe_in_all_queues
from .monitor_analyse_service import MonitorAnalyseService
from .utils import (
    get_exchange_name,
    get_receiver_routing_key,
    get_scenario,
    get_sender_routing_key,
)
from ..utils import write_log


class Observer(CommunicationService, MonitorAnalyseService, Thread):
    def __init__(self):
        self.scenarios_sequence = []
        self.adaptation_scenario = ""
        self.has_adapted = False
        self.has_adapted_uncertainty = False
        self.adaptation_status = False
        self.scenarios = []
        self.queue = ""

    def configure(self, communication, scenarios, project_name):
        CommunicationService.__init__(
            self, get_exchange_name(project_name), communication["host"]
        )
        Thread.__init__(self)
        self.scenarios = self.get_scenarios(scenarios)
        self.queue = "observer"
        self.declare_queue(self.queue)
        subscribe_in_all_queues(
            communication["host"],
            communication["user"],
            communication["password"],
            get_exchange_name(project_name),
            self.queue,
            self.channel,
        )

    def run(self):
        print(f"[*] Starting Observer")
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=False,
        )
        self.channel.start_consuming()

    def callback(self, ch, method, properties, data):
        from ..components import effector, condition

        data = json.loads(data.decode("UTF-8"))
        current_scenario = get_scenario(data, method.routing_key)

        write_log(f"Observer received: {data} from {method.routing_key}.")

        if self.analyse_normal_scenario and self.has_adapted:
            self.reset_values()
            write_log(f"System adapted successfully.")

        else:
            self.scenarios_sequence.append(current_scenario)
            result = self.analyse_adaptation_scenario(
                self.scenarios_sequence, self.scenarios["adaptation"]
            )
            if result in self.scenarios["adaptation"].keys():
                self.adaptation_scenario = result
                write_log(f"Scenario {self.adaptation_scenario} detected.")
                self.has_adapted = True
                resultA = effector.adapt(self.adaptation_scenario, "adaptation")
                if "success" in resultA.keys():
                    self.adaptation_status = True
                    self.reset_values()

            elif result == "uncertainty":
                self.has_adapted_uncertainty = True
                write_log(
                    f"Uncertainty for scenario {self.adaptation_scenario} detected."
                )
                if (
                    "success"
                    in effector.adapt(self.adaptation_scenario, "uncertainty").keys()
                ):
                    self.adaptation_status = True
                    self.reset_values()
            elif result != "wait":
                self.adaptation_status = False
                self.reset_values()
        ch.basic_ack(delivery_tag=method.delivery_tag)
        with condition:
            condition.notify_all()

    def reset_values(self):
        self.has_adapted, self.has_adapted_uncertainty = False, False
        self.scenarios_sequence = []
        self.adaptation_scenario = ""

    def get_scenarios(self, scenarios):
        new_scenarios = deepcopy(scenarios)
        for key, value in scenarios.items():
            if key == "normal":
                new_scenarios["normal"] = []
                for message in scenarios[key]:
                    new_message = deepcopy(message)
                    if "receiver" in message.keys():
                        new_message["topic"] = get_receiver_routing_key(
                            message["receiver"]
                        )
                        new_message.pop("receiver")
                    if "sender" in message.keys():
                        new_message["topic"] = get_sender_routing_key(message["sender"])
                        new_message.pop("sender")
                    new_scenarios["normal"].append(new_message)
            elif key == "adaptation":
                for scenario_name in value.keys():
                    new_scenarios["adaptation"][scenario_name] = []
                    for message in value[scenario_name]:
                        new_message = deepcopy(message)
                        if "receiver" in message.keys():
                            new_message["topic"] = get_receiver_routing_key(
                                message["receiver"]
                            )
                            new_message.pop("receiver")
                        if "sender" in message.keys():
                            new_message["topic"] = get_sender_routing_key(
                                message["sender"]
                            )
                            new_message.pop("sender")
                        new_scenarios["adaptation"][scenario_name].append(new_message)

        return new_scenarios
