from flcm.character import Character
from flcm.item import Item
from flcm.location import Location
from flcm.constants import Abilities, Professions, Gods, Books
from flcm.exceptions import (
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
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[simple_item], stamina=10, shards=15, book=Books.WTK)
    assert c.name == "Test"
    assert c.bio == "Bio"
    assert c.notes == []
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
    assert c.location == Location(1, Books.WTK)


def test_armour():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[armour], stamina=10, shards=15, book=Books.WTK)
    assert c.armour == 2


def test_defence():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[armour], stamina=10, shards=15, book=Books.WTK)
    assert c.defence == 5


def test_get_bonus():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[bonus_item], stamina=10, shards=15, book=Books.WTK)
    assert c.get_bonus(Abilities.SCOUTING) == 2


def test_add_item():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert len(c.inventory) == 0
    c.add_item(simple_item)
    assert len(c.inventory) == 1
    for x in range(11):
        c.add_item(simple_item)
    assert len(c.inventory) == 12
    with pytest.raises(InventoryFullError) as e:
        c.add_item(simple_item)


def test_remove_item():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[simple_item, simple_item], stamina=10, shards=15, book=Books.WTK)
    assert len(c.inventory) == 2
    c.remove_item(simple_item)
    assert len(c.inventory) == 1
    c.remove_item(copy_item)
    assert len(c.inventory) == 0
    with pytest.raises(ItemNotFoundError) as e:
        c.remove_item(simple_item)


def test_add_shards():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert c.shards == 15
    c.add_shards(10)
    assert c.shards == 25
    with pytest.raises(ValueError) as e:
        c.add_shards(0)
        c.add_shards(-1)


def test_spend_shards():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
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
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert c.stamina == 10
    c.damage(5)
    assert c.stamina == 5
    c.damage(6)
    assert c.stamina == 0
    with pytest.raises(ValueError) as e:
        c.damage(-1)


def test_heal():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.damage(5)
    assert c.stamina == 5
    c.heal(2)
    assert c.stamina == 7
    c.heal(4)
    assert c.stamina == 10
    with pytest.raises(ValueError) as e:
        c.heal(-1)


def test_reduce_max_stamina():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
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
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.damage(5)
    c.increase_max_stamina(5)
    assert c.max_stamina == 15
    assert c.stamina == 5
    with pytest.raises(ValueError) as e:
        c.increase_max_stamina(-1)


def test_increase_rank():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert c.rank == 1
    c.increase_rank()
    assert c.rank == 2


def test_add_note():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert c.notes == []
    c.add_note("Test note")
    assert len(c.notes) == 1
    assert c.notes[0] == "Test note"


def test_remove_note():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.add_note("Test note1")
    c.add_note("Test note2")
    c.add_note("Test note3")
    assert len(c.notes) == 3
    c.remove_note("Test note2")
    assert len(c.notes) == 2
    assert c.notes[0] == "Test note1"
    assert c.notes[1] == "Test note3"
    with pytest.raises(NoteNotFoundError) as e:
        c.remove_note("Test note4")


def test_become_initiate():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.become_initiate(Gods.SIG)
    assert c.god == Gods.SIG
    with pytest.raises(AlreadyWorshippingError) as e:
        c.become_initiate(Gods.NAGIL)


def test_revoke_worship():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.become_initiate(Gods.SIG)
    assert c.god == Gods.SIG
    c.revoke_worship()
    assert c.god == None


def test_add_blessing():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert len(c.blessings) == 0
    c.add_blessing("Test blessing")
    assert len(c.blessings) == 1
    assert c.blessings[0] == "Test blessing"


def test_remove_blessing():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    with pytest.raises(BlessingNotFoundError) as e:
        c.remove_blessing("Test blessing")
    c.add_blessing("Test blessing1")
    c.add_blessing("Test blessing2")
    c.add_blessing("Test blessing3")
    assert len(c.blessings) == 3
    c.remove_blessing("Test blessing2")
    assert len(c.blessings) == 2
    assert c.blessings[0] == "Test blessing1"
    assert c.blessings[1] == "Test blessing3"


def test_add_title():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert len(c.titles) == 0
    c.add_title("Test title")
    assert len(c.titles) == 1
    assert c.titles[0] == "Test title"


def test_remove_title():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    with pytest.raises(TitleNotFoundError) as e:
        c.remove_title("Test title")
    c.add_title("Test title1")
    c.add_title("Test title2")
    c.add_title("Test title3")
    assert len(c.titles) == 3
    c.remove_title("Test title2")
    assert len(c.titles) == 2
    assert c.titles[0] == "Test title1"
    assert c.titles[1] == "Test title3"


def test_add_resurrection():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert c.resurrection == None
    c.add_resurrection("Test resurrection")
    assert c.resurrection == "Test resurrection"


def test_deposit():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    assert c.banked_shards == 0
    assert c.shards == 15
    c.deposit(10)
    assert c.banked_shards == 10
    assert c.shards == 5
    with pytest.raises(NotEnoughShardsError) as e:
        c.deposit(10)


def test_withdraw():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.deposit(10)
    assert c.banked_shards == 10
    assert c.shards == 5
    c.withdraw(5)
    assert c.banked_shards == 5
    assert c.shards == 10
    with pytest.raises(NotEnoughShardsError) as e:
        c.withdraw(10)


def test_invest():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    l = Location(100, Books.WTK)
    c.invest(10, l)
    assert c.investments[str(l)] == 10
    assert c.shards == 5
    with pytest.raises(NotEnoughShardsError) as e:
        c.invest(10, l)


def test_disinvest():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    l = Location(100, Books.WTK)
    l2 = Location(200, Books.WTK)
    c.invest(10, l)
    c.disinvest(5, l)
    assert c.investments[str(l)] == 5
    assert c.shards == 10
    with pytest.raises(NotEnoughShardsError) as e:
        c.disinvest(10, l)
    with pytest.raises(NoInvestmentError) as e:
        c.disinvest(10, l2)
    c.update_investment(l, -10)
    assert c.investments[str(l)] == 4.5
    c.disinvest(3, l)
    assert c.investments[str(l)] == 1.5
    c.disinvest(1, l)
    assert not l in c.investments


def test_update_investment():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    l = Location(100, Books.WTK)
    c.invest(10, l)
    c.update_investment(l, -50)
    assert c.investments[str(l)] == 5
    c.update_investment(l, 10)
    assert c.investments[str(l)] == 5.5
    c.update_investment(l, 200)
    assert c.investments[str(l)] == 16.5


def test_checkboxes():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    l = Location(100, Books.WTK)
    assert c.checkboxes == {}
    c.add_checkbox(l)
    assert c.checkboxes[str(l)] == 1
    c.add_checkbox(l)
    assert c.checkboxes[str(l)] == 2
    c.remove_checkbox(l)
    assert c.checkboxes[str(l)] == 1
    c.remove_checkbox(l)
    with pytest.raises(NoCheckboxError) as e:
        c.remove_checkbox(l)


def test_add_codeword():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.add_codeword("test1")
    assert len(c.codewords) == 1
    c.add_codeword("test2")
    c.add_codeword("test3")
    assert len(c.codewords) == 3
    c.remove_codeword("test2")
    assert len(c.codewords) == 2
    assert c.codewords[0] == "test1"
    assert c.codewords[1] == "test3"
    c.add_codeword("test3")
    assert len(c.codewords) == 2



def test_store_shards():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    l = Location(100, Books.WTK)
    c.store_shards(10, l)
    assert c.shards == 5
    assert c.storage[str(l)].shards == 10
    with pytest.raises(NotEnoughShardsError) as e:
        c.store_shards(10, l)


def test_store_item():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.add_item(simple_item)
    l = Location(100, Books.WTK)
    c.store_item(simple_item, l)
    assert simple_item not in c.inventory
    assert simple_item in c.storage[str(l)].items
    with pytest.raises(ItemNotFoundError) as e:
        c.store_item(bonus_item, l)


def test_retrieve_shards():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    l = Location(100, Books.WTK)
    c.store_shards(10, l)
    c.retrieve_shards(5, l)
    assert c.shards == 10
    assert c.storage[str(l)].shards == 5
    with pytest.raises(NotEnoughShardsError) as e:
        c.retrieve_shards(10, l)



def test_retrieve_item():
    c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[], stamina=10, shards=15, book=Books.WTK)
    c.add_item(simple_item)
    l = Location(100, Books.WTK)
    c.store_item(simple_item, l)
    c.retrieve_item(simple_item, l)
    assert simple_item in c.inventory
    assert simple_item not in c.storage[str(l)].items
    with pytest.raises(ItemNotFoundError) as e:
        c.retrieve_item(bonus_item, l)
