from dataclasses import dataclass
from dataclasses import field
from enum import Enum
import sqlite3
from typing import Optional


class Category(Enum):
    potion: int = 1
    scroll: int = 2
    gold: int = 3
    weapon: int = 4
    ally: int = 5
    food: int = 6
    staff: int = 7
    ring: int = 8
    armor: int = 9
    wand: int = 10
    key: int = 11
    altar: int = 12
    charm: int = 13

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.value


class Runic(Enum):
    abomination_immunity: int = 1
    abomination_slaying: int = 2
    absorption: int = 3
    airborne_immunity: int = 4
    airborne_slaying: int = 5
    animal_immunity: int = 6
    animal_slaying: int = 7
    burden: int = 8
    confusion: int = 9
    dampening: int = 10
    dar_immunity: int = 11
    dar_slaying: int = 12
    dragon_immunity: int = 13
    dragon_slaying: int = 14
    fireborne_immunity: int = 15
    fireborne_slaying: int = 16
    force: int = 17
    goblin_immunity: int = 18
    goblin_slaying: int = 19
    immolation: int = 20
    infernal_immunity: int = 21
    infernal_slaying: int = 22
    jelly_immunity: int = 23
    jelly_slaying: int = 24
    mage_immunity: int = 25
    mage_slaying: int = 26
    mercy: int = 27
    multiplicity: int = 28
    mutuality: int = 29
    ogre_immunity: int = 30
    ogre_slaying: int = 31
    paralysis: int = 32
    plenty: int = 33
    quietus: int = 34
    reflection: int = 35
    reprisal: int = 36
    respiration: int = 37
    slowing: int = 38
    speed: int = 39
    troll_immunity: int = 40
    troll_slaying: int = 41
    turret_immunity: int = 42
    turret_slaying: int = 43
    undead_immunity: int = 44
    undead_slaying: int = 45
    vulnerability: int = 46
    waterborne_immunity: int = 47
    waterborne_slaying: int = 48

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.value


class Kind(Enum):
    aggravate_monsters: int = 1
    awareness: int = 2
    axe: int = 3
    banded_mail: int = 4
    beckoning: int = 5
    blinking: int = 6
    broadsword: int = 7
    cage_key: int = 8
    caustic_gas: int = 9
    centaur: int = 10
    chain_mail: int = 11
    clairvoyance: int = 12
    commutation_altar: int = 13
    confusion: int = 14
    conjuration: int = 15
    creeping_death: int = 16
    crystal_orb: int = 17
    dagger: int = 18
    dar_battlemage: int = 19
    dar_blademaster: int = 20
    dar_priestess: int = 21
    darkness: int = 22
    descent: int = 23
    detect_magic: int = 24
    discord: int = 25
    domination: int = 26
    door_key: int = 27
    dragon: int = 28
    empowerment: int = 29
    enchanting: int = 30
    entrancement: int = 31
    fire_immunity: int = 32
    firebolt: int = 33
    flail: int = 34
    goblin: int = 35
    goblin_conjurer: int = 36
    goblin_mystic: int = 37
    gold_pieces: int = 38
    golem: int = 39
    guardian: int = 40
    hallucination: int = 41
    haste: int = 42
    healing: int = 43
    health: int = 44
    identify: int = 45
    ifrit: int = 46
    imp: int = 47
    incendiary_dart: int = 48
    incineration: int = 49
    invisibility: int = 50
    javelin: int = 51
    leather_armor: int = 52
    levitation: int = 53
    life: int = 54
    light: int = 55
    lightning: int = 56
    mace: int = 57
    magic_mapping: int = 58
    mango: int = 59
    mangrove_dryad: int = 60
    monkey: int = 61
    naga: int = 62
    negation: int = 63
    obstruction: int = 64
    ogre: int = 65
    paralysis: int = 66
    phoenix_egg: int = 67
    pixie: int = 68
    plate_armor: int = 69
    plenty: int = 70
    poison: int = 71
    polymorphism: int = 72
    protect_armor: int = 73
    protect_weapon: int = 74
    protection: int = 75
    rapier: int = 76
    ration_of_food: int = 77
    reaping: int = 78
    recharging: int = 79
    regeneration: int = 80
    remove_curse: int = 81
    resurrection_altar: int = 82
    salamander: int = 83
    sanctuary: int = 84
    scale_mail: int = 85
    shattering: int = 86
    slowness: int = 87
    spear: int = 88
    speed: int = 89
    splint_mail: int = 90
    stealth: int = 91
    strength: int = 92
    summon_monsters: int = 93
    sword: int = 94
    telepathy: int = 95
    teleportation: int = 96
    tentacle_horror: int = 97
    transference: int = 98
    troll: int = 99
    tunneling: int = 100
    unicorn: int = 101
    war_axe: int = 102
    war_hammer: int = 103
    war_pike: int = 104
    whip: int = 105
    wisdom: int = 106
    wraith: int = 107

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.value


@dataclass(frozen=True)
class CatalogObject:
    seed: int
    depth: int
    quantity: int
    category: Category
    kind: str
    enchantment: Optional[int] = field(default=None)
    runic: Optional[Runic] = field(default=None)
    vault_number: Optional[int] = field(default=None)
    opens_vault: Optional[int] = field(default=None)
    carried_by_monster_name: Optional[str] = field(default=None)
    ally_status_name: Optional[str] = field(default=None)
    mutation_name: Optional[str] = field(default=None)

    @staticmethod
    def from_csv_row(fields: list[str]):
        kind = fields[5].replace(" ", "_")
        if kind.startswith("gold_pieces"):
            kind = "gold_pieces"
        kind = Kind[kind]
        enchantment = None if fields[6] is None else int(fields[6])
        runic = None if fields[7] is None else Runic[fields[7].replace(" ", "_")]
        vault_number = None if fields[8] is None else int(fields[8])
        opens_vault = None if fields[9] is None else int(fields[9])
        # fields[0] is dungeon_version
        return CatalogObject(
            seed=int(fields[1]),
            depth=int(fields[2]),
            quantity=int(fields[3]),
            category=Category[fields[4]],
            kind=kind,
            enchantment=enchantment,
            runic=runic,
            vault_number=vault_number,
            opens_vault=opens_vault,
            carried_by_monster_name=fields[10],
            ally_status_name=fields[11],
            mutation_name=fields[12],
        )


@dataclass(frozen=True)
class CatalogMetadata:
    dungeon_version: str
    max_depth: int
    min_seed: int
    max_seed: int


@dataclass(frozen=True)
class Catalog:
    catalog_metadata: CatalogMetadata
    catalog_objects: tuple[CatalogObject]
