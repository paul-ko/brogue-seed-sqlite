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
        enchantment = None if fields[6] is None else int(fields[6])
        vault_number = None if fields[8] is None else int(fields[8])
        opens_vault = None if fields[9] is None else int(fields[9])
        runic = None if fields[7] is None else Runic[fields[7].replace(" ", "_")]
        # fields[0] is dungeon_version
        return CatalogObject(
            seed=int(fields[1]),
            depth=int(fields[2]),
            quantity=int(fields[3]),
            category=Category[fields[4]],
            kind=fields[5],
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
