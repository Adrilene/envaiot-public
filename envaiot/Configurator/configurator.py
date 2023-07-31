import os
from time import sleep

from dotenv import load_dotenv
from flask import jsonify, request, send_file
from threading import Thread

from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator
from .assert_scenario import AssertScenario

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
            simulator.configure(
                configuration["resources"],
                configuration["project"],
                configuration["communication"],
            )
        else:
            result["simulator"] = errors_simulator

        if not errors_adapter:
            write_log(f"Adapter modeling is correct. Starting to configurate...")
            observer.configure(
                configuration["communication"],
                configuration["scenarios"],
                configuration["project"],
            )
            observer.start()
            effector.configure(configuration["strategies"])

        else:
            result["adapter"] = errors_adapter

        if result:
            return {"errors": result}

        assert_scenario = AssertScenario(configuration["scenarios"]["adaptation"])
        assert_scenario.start()
        sleep(2)
        return assert_scenario.assert_result

    def configure_simulator(self, configuration):
        from ..components import simulator

        errors = validate_simulator(configuration)
        result = {}

        if not errors:
            write_log(f"Simulator modeling is correct. Starting to configurate...")
            result["simulator"] = simulator.configure(
                configuration["resources"],
                configuration["project"],
                configuration["communication"],
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
            observer.start()
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
