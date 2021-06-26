import json

from .items import Item

class Abilities:

    def __init__(self, abilities_dict):
        self.charisma = abilities_dict["charisma"]
        self.combat = abilities_dict["combat"]
        self.magic = abilities_dict["magic"]
        self.sanctity = abilities_dict["sanctity"]
        self.scouting = abilities_dict["scouting"]
        self.thievery = abilities_dict["thievery"]


class Character:

    def __init__(self, name, profession, rank, abilities, inventory, stamina, shards):

        self.name = name
        self.profession = profession
        self.rank = rank
        self.abilities = abilities
        self.inventory = inventory
        self.stamina = stamina
        self.shards = shards


    @property
    def defence(self):
        return self.abilities.combat + self.rank + self.armour


    @property
    def armour(self):
        return self.get_bonus("defence")


    def get_bonus(self, ability):
        bonus = 0
        for item in self.inventory:
            if item.ability == ability:
                if item.value > bonus:
                    bonus = item.value
        return bonus
