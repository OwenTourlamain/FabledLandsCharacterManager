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

    def __init__(self, name, profession, rank):

        self.name = name
        self.profession = profession
        self.rank = int(rank)
        self.abilities = self.get_abilities(self.profession, rank)
        self.inventory = self.get_starting_items(self.profession, rank)
        self.stamina = self.get_stamina(self.profession, rank)
        self.shards = self.get_shards(self.profession, rank)


    @property
    def defence(self):
        return self.abilities.combat + self.rank + self.armour


    @property
    def armour(self):
        return self.get_bonus("defence")


    def get_abilities(self, profession, rank):
        with open("flcm/professions.json") as file:
            professions = json.loads(file.read())

        return Abilities(professions[rank][profession])


    def get_starting_items(self, profession, rank):
        with open("flcm/professions.json") as file:
            professions = json.loads(file.read())

        ret = []
        for item in professions[rank]["items"]:
            i = Item(item["name"], item["ability"], item["value"])
            ret.append(i)
        return ret


    def get_stamina(self, profession, rank):
        with open("flcm/professions.json") as file:
            professions = json.loads(file.read())

        return professions[rank]["stamina"]


    def get_shards(self, profession, rank):
        with open("flcm/professions.json") as file:
            professions = json.loads(file.read())

        return professions[rank]["shards"]


    def get_bonus(self, ability):
        bonus = 0
        for item in self.inventory:
            if item.ability == ability:
                if item.value > bonus:
                    bonus = item.value
        return bonus
