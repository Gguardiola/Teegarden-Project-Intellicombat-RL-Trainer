def build_action_maps(data):
    all_actions = set(d["action"] for d in data)

    special_actions = ["shield", "skip"]

    specials = [a for a in special_actions if a in all_actions]
    others = sorted(a for a in all_actions if a not in special_actions)

    ordered_actions = specials + others

    action_to_index = {a: i for i, a in enumerate(ordered_actions)}
    index_to_action = {i: a for a, i in action_to_index.items()}
    
    return action_to_index, index_to_action
