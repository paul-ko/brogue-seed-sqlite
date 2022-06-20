import dataclasses
from dataclasses import dataclass
from dataclasses import field
import itertools
from typing import Optional
from typing import Sequence


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
        vault_number = None if fields[8] == "" else int(fields[8])
        opens_vault = None if fields[9] == "" else int(fields[9])
        # fields[0] is dungeon_version
        return CatalogObject(
            seed=int(fields[1]),
            depth=int(fields[2]),
            quantity=int(fields[3]),
            category=fields[4],
            kind=fields[5],
            enchantment=enchantment,
            runic=fields[7],
            vault_number=vault_number,
            opens_vault=opens_vault,
            carried_by_monster_name=fields[10],
            ally_status_name=fields[11],
            mutation_name=fields[12],
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
