import os
from multiprocessing.dummy import Pool
from time import sleep

import requests
from dotenv import load_dotenv
from flask import jsonify, request, send_file
from project import app

from .utils import write_log, get_exchange_name
from .validator_adapter import validate_adapter
from .validator_simulator import validate_simulator
from .assert_scenario import assert_scenario

from .Configurator.configurator import Configurator
from .Simulator.simulator import Simulator
from .Observer.observer import Observer
from .Effector.effector import Effector

devices = []


load_dotenv()

configurator = Configurator()
simulator = Simulator()
observer = Observer()
effector = Effector()


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure_all", methods=["POST"])
def configure_all():
    configuration = dict(request.json)
    write_log(f"Starting {configuration['project']}...")
    errors_simulator, errors_adapter = configurator.configure_all(configuration)

    result = {}

    if not errors_simulator:
        write_log(f"Simulator modeling is correct. Starting to configurate...")
        result["simulator"] = simulator.configure(
            configuration["resources"], configuration["project"]
        )
    else:
        result["simulator"] = errors_simulator

    if not errors_adapter:
        write_log(f"Adapter modeling is correct. Starting to configurate...")
        result["adapter"]["observer"] = observer.configure(
            configuration["communication"],
            configuration["scenarios"],
            configuration["project"],
        )
        result["adapter"]["effector"] = effector.configure(configuration["strategies"])

    else:
        result["adapter"] = errors_adapter

    return jsonify(result), 200


@app.route("/configure_simulator", methods=["POST"])
def configure_simulator():
    write_log(f"Configuring Simulator...")

    configuration = dict(request.json)
    errors_simulator = configurator.configure_simulator(configuration)

    result = {}

    if not errors_simulator:
        write_log(f"Simulator modeling is correct. Starting to configurate...")
        result["simulator"] = simulator.configure(
            configuration["resources"], configuration["project"]
        )
    else:
        result["simulator"] = errors_simulator

    return jsonify(result), 200


@app.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    write_log(f"Configuring Adapter...")

    configuration = dict(request.json)
    errors_adapter = configurator.configure_adapter(configuration)
    result = {}

    if not errors_adapter:
        write_log(f"Adapter modeling is correct. Starting to configurate...")
        result["adapter"]["observer"] = observer.configure(
            configuration["communication"],
            configuration["scenarios"],
            configuration["project"],
        )
        result["adapter"]["effector"] = effector.configure(configuration["strategies"])

    else:
        result["adapter"] = errors_adapter

    return jsonify(result), 200


@app.route("/validate_scenario", methods=["POST"])
def validate_scenario():
    return jsonify(configurator.assert_scenario(request.json))


@app.route("/get_logs", methods=["GET"])
def get_logs():
    return send_file(f'{os.getenv("LOGS_PATH")}', as_attachment=True)
