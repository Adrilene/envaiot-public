import os
from multiprocessing.dummy import Pool
from time import sleep

import requests
from dotenv import load_dotenv
from flask import jsonify, request, send_file
from Configurator import app

from .utils import write_log, get_exchange_name
from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator
from .assert_scenario import assert_scenario

from ..Simulator.simulator import Simulator

devices = []


load_dotenv()


class Configurator:
    def configure_simulator(self, configuration):
        print(f"Starting {configuration['project']}...")
        errors = validate_simulator(configuration)
        if errors:
            return jsonify(errors), 400

        print("Modelling is correct. Starting to configure simulator...")
        result = requests.post(
            f"{os.getenv('SIMULATOR_HOST')}/configure", json=configuration
        )
        if result.status_code == 200:
            write_log(f"Simulator configurated with:")
            write_log(f"{configuration}\n")
            return jsonify("Simulator set!")

        return result

    def configure_adapter(self, configuration):
        configuration = dict(request.json)
        print(f"Starting {configuration['project']}...")
        errors = validate_adapter(configuration)
        if errors:
            return jsonify(errors), 400

        write_log(f"Modelling is correct. Starting to configure adapter...")

        result = {}
        observer_configuration = {
            "project": configuration["project"],
            "communication": configuration["communication"],
            "scenarios": configuration["scenarios"],
        }
        effector_configuration = {
            "strategies": configuration["strategies"],
        }
        result["Observer"] = requests.post(
            f"{os.getenv('OBSERVER_HOST')}/configure",
            json=observer_configuration,
        )
        result["Effector"] = requests.post(
            f"{os.getenv('EFFECTOR_HOST')}/configure",
            json=effector_configuration,
        )

        if (
            result["Observer"].status_code == 200
            and result["Effector"].status_code == 200
        ):
            write_log(f"Adapter configurated with:")
            write_log(f"Observer: {observer_configuration}")
            write_log(f"Effector {effector_configuration}")
            return jsonify("Adapter set!")

        response = {}
        for key, value in result.items():
            response[key] = value.json()

        return jsonify(response), 400

    def configure_all(self, configuration):
        errors_simulator = validate_simulator(configuration)
        errors_adapater = validate_adapter(configuration)

        return errors_simulator, errors_adapater

    def validate_scenario():
        return jsonify(assert_scenario(request.json))

    def get_logs():
        return send_file(f'{os.getenv("LOGS_PATH")}', as_attachment=True)
