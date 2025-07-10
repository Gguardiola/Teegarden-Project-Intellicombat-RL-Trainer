import time
import random
import json
import yaml
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '.'))
sys.path.insert(0, root_dir)

from engine.rewards import compute_reward


def load_ability_data(yaml_path):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    for ability in data:
        ability.setdefault("damage", 0)
        ability.setdefault("amount", 0)
        ability.setdefault("cost", 0)
        ability.setdefault("ignoreShield", 0)

    return data


def convert_log_to_rl_format(combat_log, ability_data, winner):
    rl_dataset = []
    enemy_turn_indices = []

    for i in range(len(combat_log) - 1):
        current = combat_log[i]
        next_step = combat_log[i + 1]

        actor = current["actor"]
        opponent = "enemy" if actor == "player" else "player"

        if actor != "enemy":
            continue

        enemy_turn_indices.append(len(rl_dataset))

        current_actor_shield = 1 if current["isShieldAction"] else 0
        opponent_shield = 1 if i > 0 and combat_log[i - 1]["actor"] == opponent and combat_log[i - 1]["isShieldAction"] else 0

        state = {
            "actor": actor,
            "actorHP": current["actorHP"],
            "actorEnergy": current["actorEnergy"],
            "actorShield": current_actor_shield,
            "opponent": opponent,
            "opponentHP": current["opponentHP"],
            "opponentEnergy": current["opponentEnergy"],
            "opponentShield": opponent_shield
        }

        next_actor_shield = 1 if next_step["actor"] == actor and next_step["isShieldAction"] else 0
        next_opponent_shield = 1 if next_step["actor"] == opponent and next_step["isShieldAction"] else 0

        next_state = {
            "actor": actor,
            "actorHP": next_step["actorHP"] if next_step["actor"] == actor else current["actorHP"],
            "actorEnergy": next_step["actorEnergy"] if next_step["actor"] == actor else current["actorEnergy"],
            "actorShield": next_actor_shield,
            "opponent": opponent,
            "opponentHP": next_step["opponentHP"] if next_step["actor"] == opponent else current["opponentHP"],
            "opponentEnergy": next_step["opponentEnergy"] if next_step["actor"] == opponent else current["opponentEnergy"],
            "opponentShield": next_opponent_shield
        }

        action = current["abilityUsed"]
        ability = next((a for a in ability_data if a['name'].lower() == action.lower()), None)

        if ability is None:
            print(f"Warning: ability '{action}' not found in ability_data. Skipping.")
            continue

        reward = compute_reward(state, next_state, action, ability_data)

        rl_dataset.append({
            "state": state,
            "action": action,
            "reward": reward,
            "next_state": next_state
        })

    if winner != "enemy" and enemy_turn_indices:
        last_enemy_index = enemy_turn_indices[-1]
        rl_dataset[last_enemy_index]["reward"] = 0

    return rl_dataset



if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '.'))

    raw_logs_dir = os.path.join(current_dir, "raw_logs")
    output_dir = os.path.join(current_dir, "training_converted_real_logs")
    os.makedirs(output_dir, exist_ok=True)

    ability_data = load_ability_data(os.path.join(root_dir, "data", "abilities.yaml"))

    for filename in os.listdir(raw_logs_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(raw_logs_dir, filename)
            with open(input_path, "r") as f:
                log = json.load(f)

            if "turns" not in log:
                print(f"Skipping {filename}: no 'turns' key.")
                continue

            winner = log.get("winner", "")
            dataset = convert_log_to_rl_format(log["turns"], ability_data, winner)

            timestamp = int(time.time() * 1000)
            rand_suffix = random.randint(1000, 9999)
            output_filename = f"real_combat_log_{timestamp}_{rand_suffix}.json"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "w") as out_f:
                json.dump(dataset, out_f, indent=2)

            print(f"Converted {filename} -> {output_filename}")