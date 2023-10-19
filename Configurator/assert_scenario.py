import os
from time import sleep
from copy import deepcopy

import requests
from dotenv import load_dotenv

from .utils import write_log

load_dotenv()


def analyse_result(scenario):
    with open(f"../{os.getenv('LOGS_PATH')}", "r") as f:
        lines = f.readlines()
        for line in lines:
            if scenario in line and "success" in line:
                return 200
        return 400


def send_message(scenario):
    from ..Simulator.simulator import Simulator

    results = []
    message = deepcopy(scenario)
    message["body"] = scenario["body"] if "body" in scenario.keys() else ""
    if "receiver" in scenario:
        message["to"] = scenario["receiver"]
        receiver = message.pop("receiver")
        result = Simulator.send_message(receiver, message)
        results.append(200 if "success" in result.keys() else 400)
    elif "sender" in scenario:
        sender = message.pop("sender")
        result = Simulator.send_message(sender, message)
        results.append(200 if "success" in result.keys() else 400)

    return results


def assert_scenario(scenarios):
    msg = []
    for scenario_name in scenarios["adaptation"].keys():
        results = []
        count = 1
        write_log(f"Asserting scenario {scenario_name}...")

        for scenario in scenarios["adaptation"][scenario_name]["scenario"]:
            results.extend(send_message(scenario))
            count += 1
            sleep(count + 1)

        sleep(5)

        results.append(analyse_result(scenario_name))

        result = ""

        if results.count(200) == len(results):
            if scenarios["adaptation"][scenario_name]["cautious"]:
                for scenario in scenarios["normal"]:
                    results.extend(send_message(scenario))
                    sleep(1)
                result = analyse_result("Cautious")
                if result == 200:
                    result = f"[SUCCESS] Scenario {scenario_name} passed and the cautious adaptation was applied."
                else:
                    result = f"[SUCCESS] Scenario {scenario_name} passed and the cautious adaptation was not applied."

            else:
                result = f"[SUCCESS] Scenario {scenario_name} passed."
        else:
            result = f"[FAILED] Scenario {scenario_name} failed."

        write_log(result)
        msg.append(result)

    return msg
