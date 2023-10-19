import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file

from components import configurator, observer, effector, simulator
from utils import write_log

application = Flask(__name__)

load_dotenv()


@application.route("/", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@application.route("/configure_all", methods=["POST"])
def configure_all():
    f = open(f"{os.getenv('LOGS_PATH')}", "w")
    f.write("")

    configuration = dict(request.json)
    result = configurator.configure_all(configuration, simulator, observer, effector)
    if type(result) is not dict:
        write_log("All components configured correctly.")
        return jsonify(result)

    return jsonify(result), 400


@application.route("/configure_simulator", methods=["POST"])
def configure_simulator():
    write_log(f"Configuring Simulator...")

    configuration = dict(request.json)
    result = configurator.configure_simulator(configuration, simulator)

    if not result:
        write_log("All components configured correctly.")
        return jsonify({"msg": "ok"})

    return jsonify(result), 400


@application.route("/configure_adapter", methods=["POST"])
def configure_adapter():
    write_log(f"Configuring Adapter...")

    configuration = dict(request.json)
    result = configurator.configure_adapter(configuration, observer, effector)

    if not result:
        write_log("All components configured correctly.")
        return jsonify({"msg": "ok"})

    return jsonify(result), 400


@application.route("/validate_scenario", methods=["POST"])
def validate_scenario():
    return jsonify(configurator.assert_scenario(dict(request.json)))


@application.route("/get_logs", methods=["GET"])
def get_logs():
    return send_file(f'{os.getenv("LOGS_PATH")}', as_attachment=True)


if __name__ == "__main__":
    port = 5000
    print(f"Running EnvAIoT port:{port} \n")
    application.run(port=port, debug=True)
