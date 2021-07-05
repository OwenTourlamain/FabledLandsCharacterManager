from .item import Item
from .location import Location
from .constants import Abilities
from .exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    NotEnoughShardsError,
    NoteNotFoundError,
    AlreadyWorshippingError,
    BlessingNotFoundError,
    TitleNotFoundError,
)

class AbilitiesContainter:

    def __init__(self, abilities_dict):
        self.charisma = abilities_dict[Abilities.CHARISMA]
        self.combat = abilities_dict[Abilities.COMBAT]
        self.magic = abilities_dict[Abilities.MAGIC]
        self.sanctity = abilities_dict[Abilities.SANCTITY]
        self.scouting = abilities_dict[Abilities.SCOUTING]
        self.thievery = abilities_dict[Abilities.THIEVERY]


class Character:

    def __init__(self, name, bio, profession, rank, abilities, inventory, stamina, shards, book):

        self.name = name
        self.bio = bio
        self.profession = profession
        self.rank = rank
        self.abilities = AbilitiesContainter(abilities)
        self.inventory = inventory
        self.stamina = stamina
        self.max_stamina = stamina
        self.shards = shards

        self.notes = []
        self.blessings = []
        self.titles = []
        self.god = None
        self.resurrection = None
        self.location = Location(1, book)


    @property
    def defence(self):
        return self.abilities.combat + self.rank + self.armour


    @property
    def armour(self):
        return self.get_bonus(Abilities.DEFENCE)


    def get_bonus(self, ability):
        bonus = 0
        for item in self.inventory:
            if item.ability == ability:
                if item.value > bonus:
                    bonus = item.value
        return bonus


    def add_item(self, item):
        if len(self.inventory) > 11:
            raise InventoryFullError()
        self.inventory.append(item)


    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            raise ItemNotFoundError()


    def add_shards(self, value):
        if value < 1:
            raise ValueError()
        self.shards += value


    def spend_shards(self, value):
        if value < 1:
            raise ValueError()
        elif value > self.shards:
            raise NotEnoughShardsError()
        self.shards -= value


    def damage(self, value):
        if value < 0:
            raise ValueError()
        self.stamina -= value
        if self.stamina < 0:
            self.stamina = 0


    def heal(self, value):
        if value < 0:
            raise ValueError()
        self.stamina += value
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina


    def increase_max_stamina(self, value):
        if value < 0:
            raise ValueError()
        self.max_stamina += value


    def reduce_max_stamina(self, value):
        if value < 0:
            raise ValueError()
        self.max_stamina -= value
        if self.max_stamina < 0:
            self.max_stamina = 0
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina


    def increase_rank(self):
        self.rank += 1


    def add_note(self, note):
        self.notes.append(note)


    def remove_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
        else:
            raise NoteNotFoundError()


    def become_initiate(self, god):
        if self.god != None:
            raise AlreadyWorshippingError()
        self.god = god


    def revoke_worship(self):
        self.god = None


    def gain_blessing(self, blessing):
        self.blessings.append(blessing)


    def remove_blessing(self, blessing):
        if blessing in self.blessings:
            self.blessings.remove(blessing)
        else:
            raise BlessingNotFoundError()


    def gain_title(self, title):
        self.titles.append(title)


    def remove_title(self, title):
        if title in self.titles:
            self.titles.remove(title)
        else:
            raise TitleNotFoundError()


    def add_resurrection(self, resurrection):
        self.resurrection = resurrection
