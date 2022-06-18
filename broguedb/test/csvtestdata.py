from broguedb.app.data import CatalogObject

misc_csv_file_catalog_objects = (
    CatalogObject(1, 2, 1, "weapon", "broadsword", 0),
    CatalogObject(1, 7, 1, "armor", "leather armor", 3, "absorption", vault_number=1),
    CatalogObject(1, 3, 1, "key", "door key", opens_vault=1),
    CatalogObject(
        1, 6, 1, "staff", "obstruction", 3, carried_by_monster_name="goblin mystic"
    ),
    CatalogObject(
        1,
        26,
        1,
        "ally",
        "tentacle horror",
        ally_status_name="shackled",
        mutation_name="reflective",
    ),
)
