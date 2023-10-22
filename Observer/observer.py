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
    write_log,
)

scenarios_sequence = []
adaptation_scenario = ""
has_adapted = False
has_adapted_uncertainty = False


class Observer(CommunicationService, MonitorAnalyseService, Thread):
    def __init__(self):
        self.scenarios_sequence = []
        self.adaptation_scenario = ""
        self.has_adapted = False
        self.has_adapted_uncertainty = False
        self.adaptation_status = False
        self.scenarios = []
        self.queue = ""

    def configure(self, configuration, effector):
        CommunicationService.__init__(
            self,
            get_exchange_name(configuration["project"]),
            configuration["communication"]["host"],
        )
        Thread.__init__(self)
        self.scenarios = self.get_scenarios(configuration["scenarios"])
        self.queue = "observer"
        self.declare_queue(self.queue)
        self.effector = effector
        subscribe_in_all_queues(
            configuration["communication"]["host"],
            configuration["communication"]["user"],
            configuration["communication"]["password"],
            get_exchange_name(configuration["project"]),
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
        global scenarios_sequence, has_adapted, has_adapted_uncertainty, adaptation_scenario
        # from ..Effector.effector import Effector

        data = json.loads(data.decode("UTF-8"))
        current_scenario = get_scenario(data, method.routing_key)

        write_log(f"Observer received: {data} from {method.routing_key}.")

        scenarios_sequence.append(current_scenario)
        analysis_normal = self.analyse_normal_scenario(
            scenarios_sequence, self.scenarios["normal"]
        )

        if analysis_normal == True:
            write_log(f"System is under a normal scenario.")
            if has_adapted or has_adapted_uncertainty:
                if self.scenarios["adaptation"][adaptation_scenario]["cautious"]:
                    write_log(f"Resetting to previous state")
                    response = self.effector.return_to_previous_state()
                    if "success" in response.keys():
                        write_log("Resource reset successfully")
                    else:
                        write_log(response["fail"])
            self.reset_values()
        elif analysis_normal == "wait":
            pass
        else:
            adaptation = self.analyse_adaptation_scenario(
                scenarios_sequence, self.scenarios["adaptation"]
            )
            if adaptation in self.scenarios["adaptation"].keys():
                if adaptation != "uncertainty":
                    write_log(f"Scenario {adaptation} detected.")
                    adaptation_scenario = adaptation
                    response = self.effector.adapt(adaptation_scenario, "adaptation")
                    has_adapted = True
                    if "success" in response.keys():
                        write_log(f"Adapted for {adaptation_scenario} successfully.")
                        scenarios_sequence = []

                    else:
                        msg_log = f"Adaptation failed for {adaptation_scenario}. Adapting uncertainty..."
                        write_log(msg_log)
                        response = self.effector.adapt(
                            adaptation_scenario, "uncertainty"
                        )
                        scenarios_sequence = []
                        has_adapted_uncertainty = True
                        if "success" in response.keys():
                            write_log(
                                f"Adapted uncertainty for {adaptation_scenario} successfully."
                            )
                            scenarios_sequence = []

                        else:
                            msg_log = f"Uncertainty for {adaptation_scenario} failed."
                            write_log(msg_log)

            elif adaptation == None:
                scenarios_sequence = []

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def reset_values(self):
        global has_adapted, has_adapted_uncertainty, scenarios_sequence, adaptation_scenario

        has_adapted, has_adapted_uncertainty = False, False
        scenarios_sequence = []

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

                    new_message["body"] = (
                        message["body"] if "body" in message.keys() else ""
                    )

                    new_scenarios["normal"].append(new_message)
            elif key == "adaptation":
                for scenario_name in value.keys():
                    new_scenarios["adaptation"][scenario_name]["cautious"] = scenarios[
                        "adaptation"
                    ][scenario_name]["cautious"]
                    new_scenarios["adaptation"][scenario_name]["scenario"] = []
                    for message in value[scenario_name]["scenario"]:
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
                        new_message["body"] = (
                            message["body"] if "body" in message.keys() else ""
                        )
                        new_scenarios["adaptation"][scenario_name]["scenario"].append(
                            new_message
                        )

        return new_scenarios
