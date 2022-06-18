from dataclasses import dataclass
from dataclasses import field
from typing import Optional


@dataclass(frozen=True)
class CatalogObject:
    seed: int
    depth: int
    quantity: int
    category: str  # enum?
    kind: str
    enchantment: Optional[int] = field(default=None)
    runic: Optional[str] = field(default=None)
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
