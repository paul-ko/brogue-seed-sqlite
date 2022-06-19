from broguedb import fileutil
from broguedb.app import readcsv
from broguedb.test import csvtestdata

catalog_1_1000_26 = fileutil.get_path_relative_to_project_root(
    "test-catalogs/catalog-1-1000-26.csv"
)
catalog_misc = fileutil.get_path_relative_to_project_root(
    "test-catalogs/catalog-misc.csv"
)


def test_read_catalog_misc():
    catalog_objects = readcsv.read_file(catalog_misc)
    expected_data = csvtestdata.misc_csv_file_raw_catalog
    assert len(catalog_objects) == len(expected_data)

    for actual, expected in zip(catalog_objects, expected_data):
        assert actual == expected


# Validate we can read a relatively large file with no errors.
def test_read_1_1000_26():
    catalog_objects = readcsv.read_file(catalog_1_1000_26)
    assert len(catalog_objects) == 199586
