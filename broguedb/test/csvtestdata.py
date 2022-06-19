from broguedb.app.data import CatalogMetadata
from broguedb.app.data import CatalogObject
from broguedb.app.data import Category
from broguedb.app.data import Kind
from broguedb.app.data import Runic

misc_csv_file_catalog_objects = (
    CatalogObject(1, 2, 1, Category.weapon, Kind.broadsword, 0),
    CatalogObject(1, 3, 1, Category.key, Kind.door_key, opens_vault=1),
    CatalogObject(
        1,
        6,
        1,
        Category.staff,
        Kind.obstruction,
        3,
        carried_by_monster_name="goblin mystic",
    ),
    CatalogObject(
        1,
        7,
        1,
        Category.armor,
        Kind.leather_armor,
        3,
        Runic.absorption,
        vault_number=1,
    ),
    CatalogObject(
        1,
        26,
        1,
        Category.ally,
        Kind.tentacle_horror,
        ally_status_name="shackled",
        mutation_name="reflective",
    ),
)

misc_csv_file_metadata = CatalogMetadata("CE 1.9", max_depth=26, min_seed=1, max_seed=1)
