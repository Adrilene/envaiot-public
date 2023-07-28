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
