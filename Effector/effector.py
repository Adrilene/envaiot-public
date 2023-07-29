from ..utils import write_log

from .plan_execute_service import PlanExecuteService
from .strategies_interpretation import strategies_to_dict


class Effector(PlanExecuteService):
    def __init__(self):
        self.strategies = {}

    def configure(self, strategies):
        self.strategies = strategies_to_dict(strategies)

    def adapt(self, scenario, adapt_type):
        write_log(f"Applying {adapt_type} for {scenario}.")
        if scenario not in self.strategies.keys():
            write_log(f"{scenario} is not configured.\n")
            return "Scenario not configured."

        result = self.plan(self.strategies[scenario][adapt_type])

        for result in results:
            if result[1] == "fail":
                count_fail += 1
        if count_fail > 0:
            return {"fail": "Effector Failed"}

        return {"success": "Effector Adapted Successfully"}

    # TODO
    # def return_to_previous_state():
    #     global effector, device, current_status
    #     responses = []

    #     for result in results:
    #         if result[1] != "fail":
    #             write_log(f"Returning {result[0]} to {result[1]}...\n")
    #             responses.append(effector.execute(result[0], result[1]))

    #     return jsonify(responses)
