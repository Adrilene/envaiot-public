class MonitorAnalyseService:
    def analyse_normal_scenario(self, current_scenario, normal_scenario):
        if current_scenario == normal_scenario:
            return True

        in_current = []
        for curr_scen in current_scenario:
            if curr_scen not in normal_scenario:
                return False
            else:
                in_current.append(curr_scen)

        if len(in_current) < len(current_scenario) and len(in_current) != 0:
            return "wait"
        if len(in_current) >= len(current_scenario):
            return True

        return False

    def compare_scenarios(self, current_scenario, adaptation_scenario):
        if current_scenario == adaptation_scenario:
            return True

        in_current = []
        for curr_scen in current_scenario:
            if curr_scen not in adaptation_scenario:
                return False
            in_current.append(curr_scen)

        if len(in_current) >= len(adaptation_scenario):
            return True

        return "wait"

    def analyse_adaptation_scenario(self, current_scenario, adaptation_scenario):
        for scenario in adaptation_scenario:
            result = self.compare_scenarios(
                current_scenario, adaptation_scenario[scenario]["scenario"]
            )
            if not result:
                continue

            if result == True:
                return scenario

            return result
