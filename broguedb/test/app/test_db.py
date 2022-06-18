import sqlite3

import pytest

from broguedb.app import db
from broguedb.test import csvtestdata

misc_test_objects = csvtestdata.misc_csv_file_catalog_objects


@pytest.fixture
def initialized_in_memory_db() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    db.set_up_fresh_db(connection)
    return connection


def test_set_up_fresh_db(initialized_in_memory_db: sqlite3.Connection):
    """
    Test the DB initialization by querying Object for all columns explicitly.

    We don't use select * to validate that the columns we expect all exist.  We validate
    that no rows exist as well, because why not...
    """
    cursor = db.execute_sqlite_sql(
        initialized_in_memory_db,
        """
        select Seed
              ,Depth
              ,Quantity
              ,Category
              ,Kind
              ,Enchantment
              ,Runic
              ,VaultNumber
              ,OpensVaultNumber
              ,CarriedByMonsterName
              ,AllyStatusName
              ,MutationName
        from Object""",
    )
    assert len(cursor.fetchall()) == 0


def test_insert_single_catalog_object(initialized_in_memory_db: sqlite3.Connection):
    """Validate that when we insert 1 object, the Object table contains 1 row."""
    to_insert = [misc_test_objects[0]]
    db.insert_catalog_objects(initialized_in_memory_db, to_insert)
    select_count_cursor = db.execute_sqlite_sql(
        initialized_in_memory_db, "select count(*) from Object"
    )
    assert select_count_cursor.fetchone()[0] == 1


def test_insert_multiple_catalog_objects(initialized_in_memory_db: sqlite3.Connection):
    """Validate that when we insert 5 objects, the Object table contains 5 rows."""
    db.insert_catalog_objects(initialized_in_memory_db, misc_test_objects)
    select_count_cursor = db.execute_sqlite_sql(
        initialized_in_memory_db, "select count(*) from Object"
    )
    assert select_count_cursor.fetchone()[0] == len(misc_test_objects)
