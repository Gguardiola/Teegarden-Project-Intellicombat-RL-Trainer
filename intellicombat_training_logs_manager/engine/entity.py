class Entity:
    def __init__(self, name, hp, energy, abilities):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.energy = energy
        self.max_energy = energy
        self.abilities = abilities
        self.shield_turns = 0
        self.effects = []

    def is_alive(self):
        return self.hp > 0

    def is_shielded(self):
        return self.shield_turns > 0
