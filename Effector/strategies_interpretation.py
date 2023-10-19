def read_actions(actions):
    actions_list = []
    index = 0

    while True:
        if index >= len(actions):
            break

        if actions[index] == "ON":
            if actions[index + 2] == "STATUS":
                actions_list.append(
                    f"{actions[index+1]}:{actions[index+2]}:{actions[index+3]}"
                )
                index += 4
            elif actions[index + 2] == "MESSAGE":
                body = ""
                i = index + 3
                while i < len(actions):
                    if actions[i].isupper():
                        break
                    body += f"{actions[i]} "
                    i += 1

                actions_list.append(f"{actions[index+1]}:{actions[index+2]}:{body}")
                index = i
            continue

        if actions[index] == "OTHERWISE" or actions[index] == "IF":
            break

    return actions_list, index + 1


def strategies_to_dict(strategies):
    strategies_list = strategies.split(" ")
    strategies_dict = {}
    key, index = "", 0

    while True:
        if index >= len(strategies_list):
            break
        if strategies_list[index] == "IF":
            key = strategies_list[index + 1]
            strategies_dict[key] = {"adaptation": [], "uncertainty": []}
            index += 2
            continue

        if strategies_list[index] == "THEN":
            strategies_dict[key]["adaptation"], increment = read_actions(
                strategies_list[index + 1 :]
            )
            index += increment
            continue

        if strategies_list[index] == "OTHERWISE":
            strategies_dict[key]["uncertainty"], increment = read_actions(
                strategies_list[index + 1 :]
            )
            index += increment
            continue

        index += 1

    return strategies_dict
