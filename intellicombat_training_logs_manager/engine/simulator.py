from .actions import Action
from .logger import CombatLogger
from .rewards import compute_reward

class CombatSimulator:
    def __init__(self, player, enemy, ability_list):
        self.player = player
        self.enemy = enemy
        self.abilities = {a["name"]: a for a in ability_list}
        self.ability_list = ability_list
        self.turn = 0
        self.log = []
        self.training_data = []
        self.logger = CombatLogger("training_simulated_logs")

    def run(self):
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn += 1
            self.log.append(f"--- Turn {self.turn} ---")

            for entity, target in [(self.player, self.enemy), (self.enemy, self.player)]:
                if not entity.is_alive() or not target.is_alive():
                    break

                state = self.get_state_snapshot(entity, target)
                action_name = self.choose_action(entity)
                action_data = self.abilities[action_name]
                action = Action(action_data)

                result = action.execute(entity, target)
                self.log.append(f"{entity.name} uses {action_name}: {result}")

                if action.type != "shield" and target.shield_turns > 0:
                    target.shield_turns = 0

                next_state = self.get_state_snapshot(entity, target)

                if entity.name.lower() == "enemy":
                    reward = compute_reward(state, next_state, action_name, self.ability_list)
                    self.training_data.append((state, action_name, reward, next_state))

                if not target.is_alive():
                    self.log.append(f"{target.name} died!")
                    break

        winner = self.player.name if self.player.is_alive() else self.enemy.name

        if winner.lower() == "enemy":
            for i in reversed(range(len(self.training_data))):
                state, action_name, reward, next_state = self.training_data[i]
                if state["actor"].lower() == "enemy":
                    final_reward = compute_reward(
                        state, next_state, action_name, self.ability_list
                    )
                    self.training_data[i] = (state, action_name, final_reward, next_state)
                    break

        self.log.append(f"Winner: {winner}")
        for entry in self.training_data:
            self.logger.log(*entry)

        self.logger.close()
        return self.log





    def choose_action(self, entity):
        import random
        valid_abilities = [
            a for a in entity.abilities
            if self.abilities[a].get("cost", 0) <= entity.energy
        ]

        if valid_abilities:
            return random.choice(valid_abilities)
        else:
            return "skip"



    def get_state_snapshot(self, actor, target):
        return {
            "actor": actor.name,
            "actorHP": actor.hp,
            "actorEnergy": actor.energy,
            "actorShield": actor.shield_turns,
            "opponent": target.name,
            "opponentHP": target.hp,
            "opponentEnergy": target.energy,
            "opponentShield": target.shield_turns,
        }
