from flcm.character import Character
from flcm.item import Item
from flcm.constants import Abilities, Professions
from flcm.exceptions import InventoryFullError, ItemNotFoundError, NotEnoughShardsError

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


def test_add_shards():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    assert c.shards == 15
    c.add_shards(10)
    assert c.shards == 25
    with pytest.raises(ValueError) as e:
        c.add_shards(0)
        c.add_shards(-1)


def test_spend_shards():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    assert c.shards == 15
    c.spend_shards(10)
    assert c.shards == 5
    c.spend_shards(5)
    assert c.shards == 0
    with pytest.raises(NotEnoughShardsError) as e:
        c.spend_shards(1)
    with pytest.raises(ValueError) as e:
        c.spend_shards(0)
        c.spend_shards(-1)


def test_damage():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    assert c.stamina == 10
    c.damage(5)
    assert c.stamina == 5
    c.damage(6)
    assert c.stamina == 0
    with pytest.raises(ValueError) as e:
        c.damage(-1)


def test_heal():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    c.damage(5)
    assert c.stamina == 5
    c.heal(2)
    assert c.stamina == 7
    c.heal(4)
    assert c.stamina == 10
    with pytest.raises(ValueError) as e:
        c.heal(-1)


def test_reduce_max_stamina():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    assert c.max_stamina == 10
    assert c.stamina == 10
    c.reduce_max_stamina(5)
    assert c.max_stamina == 5
    assert c.stamina == 5
    c.damage(1)
    assert c.max_stamina == 5
    assert c.stamina == 4
    c.reduce_max_stamina(2)
    assert c.max_stamina == 3
    assert c.stamina == 3
    c.reduce_max_stamina(4)
    assert c.max_stamina == 0
    assert c.stamina == 0
    with pytest.raises(ValueError) as e:
        c.reduce_max_stamina(-1)


def test_increase_max_stamina():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    c.damage(5)
    c.increase_max_stamina(5)
    assert c.max_stamina == 15
    assert c.stamina == 5
    with pytest.raises(ValueError) as e:
        c.increase_max_stamina(-1)


def test_increase_rank():
    c = Character("Test", Professions.MAGE, 1, abilities_dict, [], 10, 15)
    assert c.rank == 1
    c.increase_rank()
    assert c.rank == 2
    c.increase_rank()
    c.increase_rank()
    c.increase_rank()
    c.increase_rank()
    c.increase_rank()
    c.increase_rank()
    c.increase_rank()
    c.increase_rank()
    assert c.rank == 10
    c.increase_rank()
    assert c.rank == 10
