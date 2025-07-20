from engine.entity import Entity
from engine.simulator import CombatSimulator
import sys
import random
import yaml

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def select_random_abilities(abilities, max_random=3):
    heals = [a["name"] for a in abilities if a.get("type") == "heal"]
    non_heals = [a["name"] for a in abilities if a.get("type") != "heal" and a["name"] not in ["skip", "shield"]]

    selected = []

    if heals:
        selected += random.sample(heals, 1)

    n_remaining = max_random - len(selected)
    selected += random.sample(non_heals, n_remaining)

    selected += ["skip", "shield"]
    return selected

if __name__ == "__main__":

    abilities = load_yaml("data/abilities.yaml")

    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage - python simulate_combats.py [N simulations]")
        sys.exit(1)

    num_simulations = int(sys.argv[1])
    print(f"Running {num_simulations} simulations...")
    for _ in range(num_simulations):
        player_abilities = select_random_abilities(abilities)
        enemy_abilities = select_random_abilities(abilities)

        player = Entity("player", hp=100, energy=100, abilities=player_abilities)
        ##enemy = Entity("enemy", hp=100, energy=100, abilities=enemy_abilities)
        enemy = Entity("enemy", hp=100, energy=100, abilities=["Precise Shot","Heal","Laser Banana","shield","skip"])

        sim = CombatSimulator(player, enemy, abilities)
        log = sim.run()

        # for line in log:
        #     print(line)

    print(f"Done! {num_simulations} simulations executed!")
