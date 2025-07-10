import os
import yaml

from intellicombat_training_logs_manager.engine.rewards import compute_reward


def load_ability_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "data", "abilities.yaml")

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    for ability in data:
        ability.setdefault("damage", 0)
        ability.setdefault("amount", 0)
        ability.setdefault("cost", 0)
        ability.setdefault("ignoreShield", 0)

    return data


def convert_log_to_rl_format(combat_log: list, winner: str) -> list:

    ability_data = load_ability_data()

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

    # Penaliza si pierde
    if winner != "enemy" and enemy_turn_indices:
        last_enemy_index = enemy_turn_indices[-1]
        rl_dataset[last_enemy_index]["reward"] = 0

    return rl_dataset
