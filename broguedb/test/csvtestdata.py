from broguedb.app.data import CatalogMetadata
from broguedb.app.data import CatalogObject
from broguedb.app.data import Category

misc_csv_file_catalog_objects = (
    CatalogObject(1, 2, 1, Category.weapon, "broadsword", 0),
    CatalogObject(1, 3, 1, Category.key, "door key", opens_vault=1),
    CatalogObject(
        1,
        6,
        1,
        Category.staff,
        "obstruction",
        3,
        carried_by_monster_name="goblin mystic",
    ),
    CatalogObject(
        1,
        7,
        1,
        Category.armor,
        "leather armor",
        3,
        "absorption",
        vault_number=1,
    ),
    CatalogObject(
        1,
        26,
        1,
        Category.ally,
        "tentacle horror",
        ally_status_name="shackled",
        mutation_name="reflective",
    ),
)

misc_csv_file_metadata = CatalogMetadata("CE 1.9", max_depth=26, min_seed=1, max_seed=1)
