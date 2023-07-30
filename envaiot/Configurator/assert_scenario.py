from threading import Thread
from ..utils import write_log


class AssertScenario(Thread):
    def __init__(self, adaptation_scenarios):
        Thread.__init__(self)
        self.adaptation_scenarios = adaptation_scenarios
        self.assert_result = []

    def run(self):
        from ..components import simulator, observer, condition

        # adaptation_scenarios = observer.scenarios["adaptation"]
        for scenario_name in self.adaptation_scenarios.keys():
            results = []
            write_log(f"Asserting scenario {scenario_name}...")
            for scenario in self.adaptation_scenarios[scenario_name]:
                message = scenario
                if "receiver" in scenario:
                    message["to"] = scenario["receiver"]
                    receiver = message.pop("receiver")
                    simulator.send_message(receiver, message).keys()
                elif "sender" in scenario:
                    sender = message.pop("sender")
                    simulator.send_message(sender, message).keys()
                with condition:
                    condition.wait()

        if observer.adaptation_status:
            results.append("Success")
        else:
            results.append("Error")

        result = ""
        if results.count("Success") >= len(results):
            result = f"[SUCCESS] Scenario {scenario_name} passed."
        else:
            result = f"[FAILED] Scenario {scenario_name} failed."

        write_log(result)
        self.assert_result.append(result)
