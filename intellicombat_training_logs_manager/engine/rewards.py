def compute_reward(state, next_state, action, ability_data=None):
    if not isinstance(state, dict) or not isinstance(next_state, dict):
        return None

    if state.get("actor") != "enemy":
        return None

    reward = 0

    actor_energy = state.get("actorEnergy", 0)
    next_actor_energy = next_state.get("actorEnergy", 0)
    actor_hp = state.get("actorHP", 0)
    next_actor_hp = next_state.get("actorHP", 0)
    actor_shield = state.get("actorShield", 0)
    next_actor_shield = next_state.get("actorShield", 0)
    opponent_hp = state.get("opponentHP", 0)
    next_opponent_hp = next_state.get("opponentHP", 0)
    opponent_shield = state.get("opponentShield", 0)

    ability = next((a for a in (ability_data or []) if a["name"].lower().strip() == action.lower().strip()), None)

    if opponent_hp > 0 and next_opponent_hp <= 0:
        reward += 100

    if actor_hp > 0 and next_actor_hp <= 0 and actor_energy >= 10 and action.lower() != "shield":
        reward -= 100

    if ability and ability.get("type") == "attack":
        if opponent_shield > 0 and not ability.get("ignoreShield", False):
            reward -= 10
        elif opponent_shield > 0 and ability.get("ignoreShield", False):
            reward += 15

        damage_done = opponent_hp - next_opponent_hp
        if damage_done > 0:
            reward += damage_done * 0.3
            if damage_done >= 20:
                reward += 5
        else:
            reward -= 2

    if action.lower() == "shield":
        if actor_hp < 30 and actor_energy >= 10:
            reward += 10
        if next_actor_shield > actor_shield and next_actor_hp == actor_hp:
            reward += 5
        elif actor_energy <= 10 and actor_hp > 80:
            reward -= 5

    if action.lower() == "skip":
        energy_gain = next_actor_energy - actor_energy
        if energy_gain > 0:
            if actor_energy >= 80:
                reward -= 8
            elif actor_energy >= 60:
                reward -= 5
            elif actor_energy >= 40:
                reward -= 2
            else:
                missing = (100 - actor_energy) / 100
                reward += round(5 * missing, 2)
        else:
            reward -= 2

    if ability and ability.get("type") == "heal":
        healed = next_actor_hp - actor_hp
        if actor_hp < 40 and healed > 0:
            reward += 15
        elif actor_hp > 80 and healed > 0:
            reward -= 10

    if ability:
        if ability.get("cost", 0) > actor_energy:
            reward -= 8

    return round(reward, 2)
