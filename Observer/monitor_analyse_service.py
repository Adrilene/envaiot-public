class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        for scenario in normal_scenario:
            equal_number = 0
            normal_keys = scenario.keys()
            for key in normal_keys:
                if key not in current_scenario.keys():
                    return False
                if current_scenario[key] == scenario[key]:
                    equal_number += 1
            if equal_number == len(normal_keys):
                return True
        return False

    def compare_scenarios(self, current_scenario, adaptation_scenario):
        if current_scenario == adaptation_scenario:
            return True

        for curr_scen in current_scenario:
            print(f"Current: {curr_scen}")
            print(f"Adaptation: {adaptation_scenario}")
            if curr_scen not in adaptation_scenario:
                return False

        if len(current_scenario) > len(adaptation_scenario):
            return "uncertainty"

        return "wait"

    def analyse_adaptation_scenario(self, current_scenario, adaptation_scenario):
        for scenario in adaptation_scenario:
            result = self.compare_scenarios(
                current_scenario, adaptation_scenario[scenario]
            )
            print(f"RESULT: {result}")
            if not result:
                continue

            if result == True:
                return scenario

            return result

        return False
