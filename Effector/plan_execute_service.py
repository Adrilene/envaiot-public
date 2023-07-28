import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from .utils import write_log

load_dotenv()


class PlanExecuteService:
    def plan(self, actions):
        device = ""
        results = []
        for action in actions:
            device, action_type, body = action.split(":")
            response = requests.get(f"{os.getenv('SIMULATOR_HOST')}/{device}/status")
            write_log(f"{device} status is {response.json()['status']}.")

            if response.json()["status"] != "inactive":
                action_result = self.execute(device, action_type, body)
                write_log(
                    f"Action performed on {device} and the result is {action_result}."
                )
                if action_result == "success":
                    results.append((device, response.json()["status"]))

                if action_result == "fail":
                    results.append((device, "fail"))
        if not results:
            write_log(f"No device available to execute the actions specified.")
            return [(device, "fail")]

        return results

    def execute(self, device, action_type, body):
        if action_type == "STATUS":
            response = requests.post(
                f"{os.getenv('SIMULATOR_HOST')}/{device}/status",
                json={"new_status": body},
            )
        elif action_type == "MESSAGE":
            response = requests.post(
                f"{os.getenv('SIMULATOR_HOST')}/{device}/send_message",
                json={"type": "status", "body": body, "to": device},
            )
        if response.status_code == 200:
            return "success"
        return "fail"
