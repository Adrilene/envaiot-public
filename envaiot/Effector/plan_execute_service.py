import os

import requests
from dotenv import load_dotenv
from ..utils import write_log

load_dotenv()


class PlanExecuteService:
    def plan(self, actions):
        from ..components import simulator

        device = ""
        results = []
        for action in actions:
            device, action_type, body = action.split(":")
            response = simulator.status(device)
            write_log(f"{device} status is {response['status']}.")

            if response["status"] != "inactive":
                action_result = self.execute(device, action_type, body)
                write_log(
                    f"Action performed on {device} and the result is {action_result}."
                )
                if action_result == "success":
                    results.append((device, response["status"]))

                if action_result == "fail":
                    results.append((device, "fail"))
        if not results:
            write_log(f"No device available to execute the actions specified.")
            return [(device, "fail")]

        return results

    def execute(self, device, action_type, body):
        from ..components import simulator

        if action_type == "STATUS":
            response = simulator.status(device, body)
        elif action_type == "MESSAGE":
            response = requests.post(
                f"{os.getenv('SIMULATOR_HOST')}/{device}/send_message",
                json={"type": "status", "body": body, "to": device},
            )
            response = simulator.send_message(
                device, {"type": "status", "body": body, "to": device}
            )
        if "Success" in response.keys():
            return "success"
        return "fail"
