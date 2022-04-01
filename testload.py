from flcm.character import Character
from flcm.item import Item
from flcm.location import Location
from flcm.constants import Abilities, Professions, Gods, Books

import json

file = "test.json"

with open(file) as f:
    j = json.loads(f.read())

c = Character()

c.load(j)
