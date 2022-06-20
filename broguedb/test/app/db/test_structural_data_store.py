from types import MappingProxyType

from broguedb.app.data import CatalogObject
from broguedb.app.db import StructuralDataStore

structural_data_store = StructuralDataStore(
    categories=MappingProxyType({"weapon": 1, "armor": 2}),
    kinds=MappingProxyType({"broadsword": 1, "leather armor": 2}),
    runics=MappingProxyType({"quietus": 1, "absorption": 2}),
    monsters=MappingProxyType({"dragon": 1, "imp": 2}),
    ally_statuses=MappingProxyType({"shackled": 1, "caged": 2}),
    mutations=MappingProxyType({"toxic": 1, "reflective": 2}),
)


def test_generate_parameters_with_all_optional_fields_null():
    catalog_object = CatalogObject(
        seed=1, depth=2, quantity=3, category="weapon", kind="broadsword"
    )
    params = structural_data_store.generate_parameters_for_catalog_object(
        catalog_object
    )
    assert params == (
        1,  # seed
        2,  # depth
        3,  # quantity
        1,  # category
        1,  # kind
        *(None for _ in range(7)),
    )


def test_generate_parameters_with_all_optional_fields_set():
    catalog_object = CatalogObject(
        seed=1,
        depth=2,
        quantity=3,
        category="weapon",
        kind="broadsword",
        enchantment=2,
        runic="quietus",
        vault_number=1,
        opens_vault=2,
        carried_by_monster_name="imp",
        ally_status_name="caged",
        mutation_name="reflective",
    )
    params = structural_data_store.generate_parameters_for_catalog_object(
        catalog_object
    )
    assert params == (
        1,  # seed
        2,  # depth
        3,  # quantity
        1,  # category
        1,  # kind
        2,  # enchantment
        1,  # runic
        1,  # vault_number
        2,  # opens_vault
        2,  # carried_by_monster
        2,  # ally_status
        2,  # mutation
    )
