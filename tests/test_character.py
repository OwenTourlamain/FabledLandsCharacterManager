from flcm.character import Character
from flcm.item import Item
from flcm.constants import Abilities, Professions
from flcm.exceptions import InventoryFullError, ItemNotFoundError

import pytest

abilities_dict = {
        Abilities.CHARISMA: 1,
        Abilities.COMBAT: 2,
        Abilities.MAGIC: 3,
        Abilities.SANCTITY: 4,
        Abilities.SCOUTING: 5,
        Abilities.THIEVERY: 6
    }

simple_item = Item("Sword")
copy_item = Item("Sword")
bonus_item = Item("Map", Abilities.SCOUTING, 2)
armour = Item("Leather", Abilities.DEFENCE, 2)

def test_init():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [simple_item], 10, 15)
    assert c.name == "Test"
    assert c.profession == Professions.MAGE
    assert c.rank == 1
    assert c.abilities.charisma == 1
    assert c.abilities.combat == 2
    assert c.abilities.magic == 3
    assert c.abilities.sanctity == 4
    assert c.abilities.scouting == 5
    assert c.abilities.thievery == 6
    assert len(c.inventory) == 1
    assert c.stamina == 10
    assert c.shards == 15

def test_armour():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [armour], 10, 15)
    assert c.armour == 2

def test_defence():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [armour], 10, 15)
    assert c.defence == 5

def test_get_bonus():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [bonus_item], 10, 15)
    assert c.get_bonus(Abilities.SCOUTING) == 2

def test_add_item():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    assert len(c.inventory) == 0
    c.add_item(simple_item)
    assert len(c.inventory) == 1
    for x in range(11):
        c.add_item(simple_item)
    assert len(c.inventory) == 12
    with pytest.raises(InventoryFullError) as e:
        c.add_item(simple_item)

def test_remove_item():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [simple_item, simple_item], 10, 15)
    assert len(c.inventory) == 2
    c.remove_item(simple_item)
    assert len(c.inventory) == 1
    c.remove_item(copy_item)
    assert len(c.inventory) == 0
    with pytest.raises(ItemNotFoundError) as e:
        c.remove_item(simple_item)
