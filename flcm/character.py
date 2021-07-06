from .item import Item
from .house import House
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
    NoInvestmentError,
    NoCheckboxError,
    NoHouseError,
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
        self.banked_shards = 0
        self.investments = {}
        self.checkboxes = {}
        self.codewords = []
        self.houses = {}


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


    def deposit(self, value):
        if value > self.shards:
            raise NotEnoughShardsError
        self.banked_shards += value
        self.shards -= value


    def withdraw(self, value):
        if value > self.banked_shards:
            raise NotEnoughShardsError
        self.banked_shards -= value
        self.shards += value


    def invest(self, value, location):
        if value > self.shards:
            raise NotEnoughShardsError
        if location in self.investments:
            self.investments[location] += value
        else:
            self.investments[location] = value
        self.shards -= value


    def disinvest(self, value, location):
        if not location in self.investments:
            raise NoInvestmentError
        if value > self.investments[location]:
            raise NotEnoughShardsError
        self.investments[location] -= value
        self.shards += value
        if self.investments[location] == 0:
            del self.investments[location]


    def update_investment(self, location, percentage):
        if not location in self.investments:
            raise NoInvestmentError
        self.investments[location] = self.investments[location] * percentage


    def add_checkbox(self, location):
        if not location in self.checkboxes:
            self.checkboxes[location] = 1
        else:
            self.checkboxes[location] += 1


    def remove_checkbox(self, location):
        if not location in self.checkboxes:
            raise NoCheckboxError
        self.checkboxes[location] -= 1
        if self.checkboxes[location] == 0:
            del self.checkboxes[location]


    def add_codeword(self, codeword):
        if not codeword in self.codewords:
            self.codewords.append(codeword)


    def remove_codeword(self, codeword):
        if codeword in self.codewords:
            self.codewords.remove(codeword)
        else:
            raise CodewordNotFoundError()


    def store_shards_in_house(self, value, location):
        if value > self.shards:
            raise NotEnoughShardsError
        if not location in self.houses:
            self.houses[location] = House()
        self.houses[location].shards += value
        self.shards -= value


    def retrieve_shards_from_house(self, value, location):
        if not location in self.houses:
            raise NoHouseError
        if value > self.houses[location].shards:
            raise NotEnoughShardsError
        self.houses[location].shards -= value
        self.shards += value


    def store_item_in_house(self, item, location):
        if not item in self.inventory:
            raise ItemNotFoundError
        if not location in self.houses:
            self.houses[location] = House()
        self.houses[location].items.append(item)
        self.remove_item(item)


    def retrieve_item_from_house(self, item, location):
        if not location in self.houses:
            raise NoHouseError
        if not item in self.houses[location].items:
            raise ItemNotFoundError
        self.add_item(item)
        self.houses[location].items.remove(item)
