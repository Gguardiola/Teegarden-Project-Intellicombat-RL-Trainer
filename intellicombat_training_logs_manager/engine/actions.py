class Action:
    def __init__(self, data):
        self.name = data["name"]
        self.type = data["type"]
        self.cost = data.get("cost", 0)
        self.data = data

    def execute(self, actor, target):
        result = {}

        actor.energy = max(0, actor.energy - self.cost)

        if self.type == "attack":
            dmg = self.data["damage"]
            ignore_shield = self.data.get("ignoreShield", False)

            if target.is_shielded() and not ignore_shield:
                dmg = 0
                target.shield_turns = 0 

            target.hp = max(0, target.hp - dmg)
            result["damage"] = dmg

            if "effect" in self.data:
                from .effects import apply_effect
                result["effect"] = apply_effect(target, self.data["effect"])

        elif self.type == "heal":
            amt = self.data["amount"]
            actor.hp = min(actor.max_hp, actor.hp + amt)
            result["heal"] = amt

        elif self.type == "shield":
            actor.shield_turns = 1
            result["shield"] = True

        elif self.type == "skip":
            recovered = self.data.get("recover", 20)
            actor.energy = min(actor.max_energy, actor.energy + recovered)
            result["energyRecovered"] = recovered

        return result
