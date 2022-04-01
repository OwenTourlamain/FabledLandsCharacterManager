from flcm.character import Character
from flcm.item import Item
from flcm.location import Location
from flcm.constants import Abilities, Professions, Gods, Books

abilities_dict = {
        Abilities.CHARISMA: 1,
        Abilities.COMBAT: 2,
        Abilities.MAGIC: 3,
        Abilities.SANCTITY: 4,
        Abilities.SCOUTING: 5,
        Abilities.THIEVERY: 6
    }

simple_item = Item("Sword")
simple_item2 = Item("Sword2")
bonus_item = Item("Map", Abilities.SCOUTING, 3)
armour = Item("Leather Armour", Abilities.DEFENCE, 1)

c = Character(name="Test", bio="Bio", profession=Professions.MAGE, rank=1, abilities=abilities_dict, inventory=[simple_item, simple_item2, bonus_item, armour], stamina=10, shards=15, book=Books.WTK)
c.add_note("note1")
c.add_note("note2")
c.add_note("note3")
c.add_note("note4")
c.add_blessing("blessing1")
c.add_blessing("blessing2")
c.add_blessing("blessing3")
c.add_blessing("blessing4")
c.add_title("title1")
c.add_title("title2")
c.add_title("title3")
c.add_title("title4")
c.add_codeword("cw1")
c.add_codeword("cw2")
c.add_codeword("cw3")
c.add_codeword("cw4")
c.add_checkbox(Location(1, Books.WTK))
c.add_checkbox(Location(1, Books.WTK))
c.add_checkbox(Location(1, Books.WTK))
c.add_checkbox(Location(2, Books.WTK))
c.add_checkbox(Location(3, Books.WTK))
c.invest(5, Location(3, Books.WTK))
c.store_item(simple_item, Location(4, Books.WTK))
c.store_item(bonus_item, Location(4, Books.WTK))
json = c.save()
with open("test.json", 'w') as f:
    f.write(json)
