def check_keys(scenarios):
    errors = []

    for scenario in scenarios.keys():
        if scenario == "normal":
            """if "sender" not in scenarios[scenario].keys() and "receiver" not in scenarios[scenario].keys():
            errors.append(f"Missing 'sender' or 'receiver' key for {scenario} scenario")
            """
            for item in scenarios[scenario]:
                if "type" not in item.keys():
                    errors.append(f"Missing 'type' key for {scenario} scenario")

        elif scenario == "adaptation":
            for key, value in scenarios[scenario].items():
                if "cautious" not in value.keys():
                    errors.append(f"Missing 'cautious' key for {key}")
                for action in value["scenario"]:
                    if "type" not in action.keys():
                        errors.append(f"Missing 'type' key for {key} scenario")
                    if "sender" not in action.keys():
                        if "receiver" not in action.keys():
                            errors.append(
                                f"Missing 'sender' or 'receiver' key for {key} scenario"
                            )
                        continue
                    continue
    return errors


def check_scenarios_names(scenarios_names):
    errors = []

    for scenario in scenarios_names:
        if (
            not scenario[0].isupper()
            and scenario != scenario.lower()
            and scenario != scenario.upper()
            and "_" not in scenario
        ):
            errors.append(f"{scenario} is not a valid scenario name")

    return errors


def check_strategies(strategies, scenarios):
    errors = []
    keywords = ["IF", "THEN", "ON", "STATUS", "MESSAGE"]

    for keyword in keywords:
        if keyword not in strategies:
            errors.append(f"Keyword {keyword} not found in strategies")

    if errors:
        return errors

    keywords.append("OTHERWISE")
    strategies_formatted = strategies.split(" ")
    scenarios_mapped = []
    for i in range(len(strategies_formatted)):
        if strategies_formatted[i] == "IF":
            scenarios_mapped.append(strategies_formatted[i + 1])

        if strategies_formatted[i] == "THEN" and strategies_formatted[i + 1] != "ON":
            errors.append(f"Missing ON after THEN")

        if (
            strategies_formatted[i].isupper()
            and strategies_formatted[i] not in keywords
        ):
            errors.append(
                f"Inappropriate use of uppercase word {strategies_formatted[i]}"
            )

    for scenario in scenarios:
        if scenario not in scenarios_mapped:
            errors.append(f"Scenario {scenario} has no action mapped")

    return errors


def validate_adapter(configuration):
    errors = []

    if "scenarios" not in configuration.keys():
        return "Missing 'scenarios' key."

    if "strategies" not in configuration.keys():
        return "Missing 'strategies' key."

    if "normal" not in configuration["scenarios"].keys():
        errors.append("Missing 'normal' key")

    if "adaptation" not in configuration["scenarios"].keys():
        errors.append("Missing 'adaptation' key")

    errors_keys = check_keys(configuration["scenarios"])
    errors_strategies = check_strategies(
        configuration["strategies"], configuration["scenarios"]["adaptation"].keys()
    )
    if errors_keys:
        errors.extend(errors_keys)
    if errors_strategies:
        errors.extend(errors_strategies)

    return errors
