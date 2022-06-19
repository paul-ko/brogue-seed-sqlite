import dataclasses
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
import itertools
import sqlite3
from typing import Optional
from typing import Sequence


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
    category: str
    kind: str
    enchantment: Optional[int] = field(default=None)
    runic: Optional[str] = field(default=None)
    vault_number: Optional[int] = field(default=None)
    opens_vault: Optional[int] = field(default=None)
    carried_by_monster_name: Optional[str] = field(default=None)
    ally_status_name: Optional[str] = field(default=None)
    mutation_name: Optional[str] = field(default=None)

    @staticmethod
    def from_csv_row(fields: Sequence[str | None]) -> "CatalogObject":
        enchantment = None if fields[6] == "" else int(fields[6])
        runic = None if fields[7] == "" else fields[7]
        vault_number = None if fields[8] == "" else int(fields[8])
        opens_vault = None if fields[9] == "" else int(fields[9])
        carried_by_monster_name = None if fields[10] == "" else fields[10]
        ally_status_name = None if fields[11] == "" else fields[11]
        mutation_name = None if fields[12] == "" else fields[12]
        # fields[0] is dungeon_version
        return CatalogObject(
            seed=int(fields[1]),
            depth=int(fields[2]),
            quantity=int(fields[3]),
            category=fields[4],
            kind=fields[5],
            enchantment=enchantment,
            runic=runic,
            vault_number=vault_number,
            opens_vault=opens_vault,
            carried_by_monster_name=carried_by_monster_name,
            ally_status_name=ally_status_name,
            mutation_name=mutation_name,
        )

    def to_csv_row_format(self, dungeon_version: str):
        iterator = itertools.chain([dungeon_version], dataclasses.astuple(self))
        return tuple(str(s) if s is not None else "" for s in iterator)


@dataclass(frozen=True)
class CatalogMetadata:
    dungeon_version: str
    max_depth: int
    min_seed: int
    max_seed: int
