from .utils import write_log

from .plan_execute_service import PlanExecuteService
from .strategies_interpretation import strategies_to_dict


results = []


class Effector(PlanExecuteService):
    def __init__(self):
        self.strategies = {}

    def configure(self, configuration):
        self.strategies = strategies_to_dict(configuration["strategies"])

    def adapt(self, scenario, adapt_type):
        global results

        write_log(f"Applying {adapt_type} for {scenario}.")
        if scenario not in self.strategies.keys():
            write_log(f"{scenario} is not configured.\n")
            return {"fail": "Scenario not configured."}

        results = self.plan(self.strategies[scenario][adapt_type])
        count_fail = 0
        for result in results:
            if result[1] == "fail":
                count_fail += 1
        if count_fail > 0:
            msg = f"{adapt_type} for {scenario} failed"
            write_log(msg)
            return {"fail": msg}

        msg = f"{adapt_type} for {scenario} applied successfully"
        return {"success": msg}

    def return_to_previous_state():
        global results

        responses = []
        for result in results:
            if result[1] != "fail":
                if result[1] == "STATUS":
                    write_log(f"Returning {result[0]} to {result[2]}...")
                    result = self.execute(result[0], result[1], result[2])
                    responses.append(result)
                    msg_log = f"Cautious adaptation result is {result}"
                    write_log(msg_log)
                    return {"success": msg_log}
                else:
                    msg = f"Not possible to apply cautious on adaptation action of the type {result[1]}"
                    write_log(msg)
                    return {"fail": msg}
