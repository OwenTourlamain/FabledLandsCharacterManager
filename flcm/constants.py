from enum import Enum

class Abilities(Enum):
    CHARISMA = "Charisma"
    COMBAT = "Combat"
    MAGIC = "Magic"
    SCOUTING = "Scouting"
    SANCTITY = "Sanctity"
    THIEVERY = "Thievery"
    DEFENCE = "Defence"


class Professions(Enum):
    PRIEST = "Priest"
    MAGE = "Mage"
    ROGUE = "Rogue"
    TROUBADOUR = "Troubadour"
    WARRIOR = "Warrior"
    WAYFARER = "Wayfarer"


class Gods(Enum):
    ALVIR_VALMIR = "Alvir and Valmir"
    ELNIR = "Elnir"
    LACUNA = "Lacuna"
    MAKA = "Maka"
    MOLHERN = "Molhern"
    NAGIL = "Nagil"
    SIG = "Sig"
    THREE_FORTUNES = "The Three Fortunes"
    TYRNAI = "Tyrnai"
