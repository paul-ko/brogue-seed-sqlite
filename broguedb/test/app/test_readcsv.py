from broguedb import fileutil
from broguedb.app import readcsv
from broguedb.app.data import CatalogObject

catalog_1_1000_26 = fileutil.get_path_relative_to_project_root(
    "test-catalogs/catalog-1-1000-26.csv"
)
catalog_misc = fileutil.get_path_relative_to_project_root(
    "test-catalogs/catalog-misc.csv"
)


def test_read_catalog_misc():
    catalog_objects = readcsv.read_file(catalog_misc)
    assert len(catalog_objects) == 5
    assert catalog_objects[0] == CatalogObject(1, 2, 1, "weapon", "broadsword", 0)
    assert catalog_objects[1] == CatalogObject(
        1, 7, 1, "armor", "leather armor", 3, "absorption", vault_number=1
    )
    assert catalog_objects[2] == CatalogObject(
        1, 3, 1, "key", "door key", opens_vault=1
    )
    assert catalog_objects[3] == CatalogObject(
        1, 6, 1, "staff", "obstruction", 3, carried_by_monster_name="goblin mystic"
    )
    assert catalog_objects[4] == CatalogObject(
        1,
        26,
        1,
        "ally",
        "tentacle horror",
        ally_status_name="shackled",
        mutation_name="reflective",
    )


# Validate we can read a relatively large file with no errors.
def test_read_1_1000_26():
    catalog_objects = readcsv.read_file(catalog_1_1000_26)
    assert len(catalog_objects) == 199586
