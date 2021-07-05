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

class Books(Enum):
    WTK = "The War-Torn Kingdom"
    CGG = "Cities of Gold and Glory"
    BDS = "Over the Blood Dark Sea"
    PHD = "The Plains of Howling Darkness"
    CHF = "The Court of Hidden Faces"
    LRS = "Lords of the Rising Sun"
    SKD = "The Serpent King's Domain"
    LLS = "The Lone and Level Sands"
    ITS = "The Isle of a Thousand Spires"
    LTL = "Legions of the Labyrinth"
    TCC = "The City in the Clouds"
    ITU = "Into the Underworld"
