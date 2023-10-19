import os
from datetime import datetime

from dotenv import load_dotenv
from flask import jsonify, request, send_file
from threading import Thread

from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator
from .assert_scenario import assert_scenario

from utils import write_log

devices = []


load_dotenv()


class Configurator:
    def configure_all(self, configuration, simulator, observer, effector):
        # from ..Simulator.simulator import Simulator
        # from ..Observer.observer import Observer
        # from ..Effector.effector import Effector

        if os.path.exists(f"../{os.getenv('LOGS_PATH')}"):
            now = datetime.now()
            new_name = f"../{os.getenv('LOGS_PATH')}".replace(
                "logs", f"logs_{now.strftime('%d%m%Y%H%M')}"
            )
            os.rename(f"../{os.getenv('LOGS_PATH')}", new_name)
        write_log(f"Starting {configuration['project']}...")
        errors_simulator = validate_simulator(configuration)

        errors_adapater = validate_adapter(configuration)

        if errors_adapater or errors_simulator:
            return {
                "errors simulator modeling": errors_simulator,
                "errors adapter modeling": errors_adapater,
            }

        simulator_configuration = {
            "project": configuration["project"],
            "resources": configuration["resources"],
            "communication": configuration["communication"],
        }

        simulator.configure(simulator_configuration)

        observer_configuration = {
            "project": configuration["project"],
            "communication": configuration["communication"],
            "scenarios": configuration["scenarios"],
        }
        observer.configure(observer_configuration)

        effector_configuration = {
            "strategies": configuration["strategies"],
        }
        effector.configure(effector_configuration)

        write_log(f"Components configured:")
        write_log(f"Simulator: {simulator_configuration}")
        write_log(f"Obsever: {observer_configuration}")
        write_log(f"Effector: {effector_configuration}")

        return assert_scenario(configuration["scenarios"])

    def validate_scenario(scenario):
        return assert_scenario(scenario)

    def get_logs():
        return send_file(
            f'{os.getcwd().split("Configurator")[0]}{os.getenv("LOGS_PATH")}',
            as_attachment=True,
        )
