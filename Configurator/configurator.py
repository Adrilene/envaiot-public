import os
from time import sleep

from dotenv import load_dotenv
from flask import jsonify, request, send_file

from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator
from .assert_scenario import assert_scenario

from ..Simulator.simulator import Simulator
from ..utils import write_log


devices = []


load_dotenv()


class Configurator:
    def configure_simulator(self, configuration):
        errors = validate_simulator(configuration)
        return errors

    def configure_adapter(self, configuration):
        errors = validate_adapter(configuration)
        return errors

    def configure_all(self, configuration):
        errors_simulator = validate_simulator(configuration)
        errors_adapater = validate_adapter(configuration)

        return errors_simulator, errors_adapater

    def validate_scenario():
        return jsonify(assert_scenario(request.json))

    def get_logs():
        return send_file(f'{os.getenv("LOGS_PATH")}', as_attachment=True)

    def assert_scenario(self, adaptation_scenarios, simulator, obsever):
        msg = []
        for scenario_name in adaptation_scenarios.keys():
            results = []
            count = 1
            write_log(f"Asserting scenario {scenario_name}...")
            for scenario in adaptation_scenarios[scenario_name]:
                message = scenario
                if "receiver" in scenario:
                    message["to"] = scenario["receiver"]
                    message["body"] = scenario["body"] if scenario["body"] else ""
                    receiver = message.pop("receiver")
                    results.append(simulator.send_message(receiver, message).keys())
                elif "sender" in scenario:
                    sender = message.pop("sender")
                    results.append(simulator.send_message(sender, message).keys())
                count += 1
                sleep(count + 1)

        if obsever.adaptation_status:
            results.append("Success")
        else:
            results.append("Error")

        result = ""
        if results.count("Success") == len(results):
            result = f"[SUCCESS] Scenario {scenario_name} passed."
        else:
            result = f"[FAILED] Scenario {scenario_name} failed."

        write_log(result)
        msg.append(result)

        return msg
