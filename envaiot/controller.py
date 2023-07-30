import os

from dotenv import load_dotenv
from flask import jsonify, request, send_file

from .utils import write_log
from .components import configurator, simulator, observer, effector

from . import app

load_dotenv()


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/configure_all", methods=["POST"])
def configure_all():
    f = open(f"./{os.getenv('LOGS_PATH')}", "w")
    f.write("")

    configuration = dict(request.json)
    result = configurator.configure_all(configuration)
    if type(result) is not dict:
        write_log("All components configured correctly.")
        return jsonify(result)

    return jsonify(result), 400


@app.route("/configure_simulator", methods=["POST"])
def configure_simulator():
    write_log(f"Configuring Simulator...")

    configuration = dict(request.json)
    result = configurator.configure_simulator(configuration)

    if not result:
        write_log("All components configured correctly.")
        return jsonify({"msg": "ok"})

    return jsonify(result), 400


@app.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    write_log(f"Configuring Adapter...")

    configuration = dict(request.json)
    result = configurator.configure_adapter(configuration)

    if not result:
        write_log("All components configured correctly.")
        return jsonify({"msg": "ok"})

    return jsonify(result), 400


@app.route("/validate_scenario", methods=["POST"])
def validate_scenario():
    return jsonify(configurator.assert_scenario(dict(request.json)))


@app.route("/get_logs", methods=["GET"])
def get_logs():
    return send_file(f'{os.getenv("LOGS_PATH")}', as_attachment=True)
