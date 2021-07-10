from math import floor
import json

from .item import Item
from .storage import Storage
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
    NoStorageError,
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

    def __init__(self, name=None, bio=None, profession=None, rank=None, abilities=None, inventory=None, stamina=None, shards=None, book=None):
        if name:
            self.name = name
            self.bio = bio
            self.profession = profession
            self.rank = rank
            self.abilities = AbilitiesContainter(abilities)
            self.inventory = inventory
            self.stamina = stamina
            self.max_stamina = stamina
            self.shards = shards
            self.location = Location(1, book)
        else:
            self.name = None
            self.bio = None
            self.profession = None
            self.rank = 0
            self.abilities = None
            self.inventory = []
            self.stamina = 0
            self.max_stamina = 0
            self.shards = 0
            self.location = None

        self.notes = []
        self.blessings = []
        self.titles = []
        self.god = None
        self.resurrection = None
        self.banked_shards = 0
        self.investments = {}
        self.checkboxes = {}
        self.codewords = []
        self.storage = {}


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
        if value < 0:
            raise ValueError()
        self.shards += value


    def spend_shards(self, value):
        if value < 0:
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


    def add_blessing(self, blessing):
        self.blessings.append(blessing)


    def remove_blessing(self, blessing):
        if blessing in self.blessings:
            self.blessings.remove(blessing)
        else:
            raise BlessingNotFoundError()


    def add_title(self, title):
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
        location = str(location)
        if value > self.shards:
            raise NotEnoughShardsError
        if location in self.investments:
            self.investments[location] += value
        else:
            self.investments[location] = value
        self.shards -= value


    def disinvest(self, value, location):
        location = str(location)
        if not location in self.investments:
            raise NoInvestmentError
        if value > self.investments[location]:
            raise NotEnoughShardsError
        self.investments[location] -= value
        self.shards += floor(value)
        if self.investments[location] < 1:
            self.investments[location] = 0
        if self.investments[location] == 0:
            del self.investments[location]


    def update_investment(self, location, percentage):
        location = str(location)
        if not location in self.investments:
            raise NoInvestmentError
        self.investments[location] = self.investments[location] * ((100 + percentage) / 100)


    def add_checkbox(self, location):
        key = str(location)
        value = 1
        if key in self.checkboxes:
            value += self.checkboxes[key]
        self.checkboxes[key] = value


    def remove_checkbox(self, location):
        key = str(location)
        if not key in self.checkboxes:
            raise NoCheckboxError
        self.checkboxes[key] -= 1
        if self.checkboxes[key] == 0:
            del self.checkboxes[key]


    def add_codeword(self, codeword):
        if not codeword in self.codewords:
            self.codewords.append(codeword)


    def remove_codeword(self, codeword):
        if codeword in self.codewords:
            self.codewords.remove(codeword)
        else:
            raise CodewordNotFoundError()


    def store_shards(self, value, location):
        location = str(location)
        if value > self.shards:
            raise NotEnoughShardsError
        if not location in self.storage:
            self.storage[location] = Storage()
        self.storage[location].shards += value
        self.shards -= value


    def retrieve_shards(self, value, location):
        location = str(location)
        if not location in self.storage:
            raise NoStorageError
        if value > self.storage[location].shards:
            raise NotEnoughShardsError
        self.storage[location].shards -= value
        self.shards += value


    def store_item(self, item, location):
        location = str(location)
        if not item in self.inventory:
            raise ItemNotFoundError
        if not location in self.storage:
            self.storage[location] = Storage()
        self.storage[location].items.append(item)
        self.remove_item(item)


    def retrieve_item(self, item, location):
        location = str(location)
        if not location in self.storage:
            raise NoStorageError
        if not item in self.storage[location].items:
            raise ItemNotFoundError
        self.add_item(item)
        self.storage[location].items.remove(item)


    def save(self):
        inventory = []
        for item in self.inventory:
            inventory.append(item.json)
        inventory = json.dumps(inventory, indent=2).replace('\n', '\n    ')
        notes = json.dumps(self.notes, indent=2).replace('\n', '\n    ')
        blessings = json.dumps(self.blessings, indent=2).replace('\n', '\n    ')
        titles = json.dumps(self.titles, indent=2).replace('\n', '\n    ')
        codewords = json.dumps(self.codewords, indent=2).replace('\n', '\n    ')
        checkboxes = json.dumps(self.checkboxes, indent=2).replace('\n', '\n    ')
        investments = json.dumps(self.investments, indent=2).replace('\n', '\n    ')
        storage = json.dumps(self.storage, default=vars, indent=2).replace('\n', '\n    ')
        if self.god:
            god = f'"{self.god}"'
        else:
            god = 'null'
        if self.resurrection:
            resurrection = f'"{self.resurrection}"'
        else:
            resurrection = 'null'

        return (
            f'{{\n'
            f'  "character": {{\n'
            f'    "name": "{self.name}",\n'
            f'    "bio": "{self.bio}",\n'
            f'    "profession": "{self.profession}",\n'
            f'    "rank": {self.rank},\n'
            f'    "stamina": {self.stamina},\n'
            f'    "max_stamina": {self.max_stamina},\n'
            f'    "abilities": {{\n'
            f'      "charisma": {self.abilities.charisma},\n'
            f'      "combat": {self.abilities.combat},\n'
            f'      "magic": {self.abilities.magic},\n'
            f'      "sanctity": {self.abilities.sanctity},\n'
            f'      "scouting": {self.abilities.scouting},\n'
            f'      "thievery": {self.abilities.thievery}\n'
            f'    }},\n'
            f'    "shards": {self.shards},\n'
            f'    "banked_shards": {self.banked_shards},\n'
            f'    "resurrection": {resurrection},\n'
            f'    "god": {god},\n'
            f'    "location": {{\n'
            f'      "book": "{self.location.book}",\n'
            f'      "section": "{self.location.section}"\n'
            f'    }},\n'
            f'    "inventory": {inventory},\n'
            f'    "notes": {notes},\n'
            f'    "blessings": {blessings},\n'
            f'    "titles": {titles},\n'
            f'    "codewords": {codewords},\n'
            f'    "checkboxes": {checkboxes},\n'
            f'    "investments": {investments},\n'
            f'    "storage": {storage}\n'
            f'  }}\n'
            f'}}'
        )


    def load(self, json):
        character = json['character']

        self.name = character['name']
        self.bio = character['bio']
        self.profession = character['profession']
        self.rank = character['rank']
        self.stamina = character['stamina']
        self.max_stamina = character['max_stamina']
        self.shards = character['shards']
        self.banked_shards = character['banked_shards']
        self.resurrection = character['resurrection']
        self.god = character['god']
        self.abilities = character['abilities']

        self.location = Location(character['location']['book'], character['location']['section'])

        for item in character['inventory']:
            i = Item(item['name'], item['ability'], item['value'])
            self.add_item(i)
        for note in character['notes']:
            self.add_note(note)
        for blessing in character['blessings']:
            self.add_blessing(blessing)
        for title in character['titles']:
            self.add_title(title)
        for codeword in character['codewords']:
            self.add_codeword(codeword)

        for checkbox in character['checkboxes']:
            value = character['checkboxes'][checkbox]
            l = checkbox.split(', section: ')
            location = Location(l[1], l[0])
            for i in range(value):
                self.add_checkbox(location)

        for investment in character['investments']:
            value = character['investments'][investment]
            l = investment.split(', section: ')
            location = Location(l[1], l[0])
            self.add_shards(value)
            self.invest(value, location)

        for storage in character['storage']:
            shards = character['storage'][storage]['shards']
            items = character['storage'][storage]['items']
            l = investment.split(', section: ')
            location = Location(l[1], l[0])
            self.add_shards(shards)
            self.store_shards(shards, location)
            self.storage[str(location)].items = []
            for item in items:
                i = Item(item['name'], item['ability'], item['value'])
                self.storage[str(location)].items.append(i)
