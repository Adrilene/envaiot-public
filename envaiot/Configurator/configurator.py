import os
from time import sleep

from dotenv import load_dotenv
from flask import jsonify, request, send_file

from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator

from ..utils import write_log


devices = []


load_dotenv()


class Configurator:
    def configure_all(self, configuration):
        from ..components import simulator, observer, effector

        errors_simulator = validate_simulator(configuration)
        errors_adapter = validate_adapter(configuration)
        result = {}

        if not errors_simulator:
            write_log(f"Simulator modeling is correct. Starting to configurate...")
            simulator.configure(configuration["resources"], configuration["project"])
        else:
            result["simulator"] = errors_simulator

        if not errors_adapter:
            write_log(f"Adapter modeling is correct. Starting to configurate...")
            observer.configure(
                configuration["communication"],
                configuration["scenarios"],
                configuration["project"],
            )
            effector.configure(configuration["strategies"])

        else:
            result["adapter"] = errors_adapter

        if result:
            return result

    def configure_simulator(self, configuration):
        from ..components import simulator

        errors = validate_simulator(configuration)
        result = {}

        if not errors:
            write_log(f"Simulator modeling is correct. Starting to configurate...")
            result["simulator"] = simulator.configure(
                configuration["resources"], configuration["project"]
            )
        else:
            result["simulator"] = errors

        if result:
            return result

    def configure_adapter(self, configuration):
        from ..components import observer, effector

        errors = validate_adapter(configuration)
        result = {}

        if not errors:
            write_log(f"Adapter modeling is correct. Starting to configurate...")
            result["adapter"]["observer"] = observer.configure(
                configuration["communication"],
                configuration["scenarios"],
                configuration["project"],
            )
            result["adapter"]["effector"] = effector.configure(
                configuration["strategies"]
            )

        else:
            result["adapter"] = errors

        if result:
            return result

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
