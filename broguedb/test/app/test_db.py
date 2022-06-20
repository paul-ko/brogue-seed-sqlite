import sqlite3

import pytest

from broguedb.app import db
from broguedb.app.db import DBService
from broguedb.test import csvtestdata

misc_test_objects = csvtestdata.misc_csv_file_catalog_objects
misc_test_metadata = csvtestdata.misc_csv_file_catalog_metadata
misc_test_catalog = csvtestdata.misc_csv_file_catalog


@pytest.fixture
def initialized_in_memory_db() -> DBService:
    connection = sqlite3.connect(":memory:")
    service = db.DBService(connection, is_new_db=True)
    service.prepare_db()
    service.populate_structural_data(misc_test_catalog)
    return service


def test_run_ddl(initialized_in_memory_db: DBService):
    """
    Test the DB initialization by querying for all tables, views, and columns.

    We don't use select * to validate that the columns we expect all exist.
    """
    connection = initialized_in_memory_db.connection
    db.execute_sqlite_sql(
        connection,
        """
        select Seed
              ,Depth
              ,Quantity
              ,CategoryID
              ,KindID
              ,Enchantment
              ,RunicID
              ,VaultNumber
              ,OpensVaultNumber
              ,CarriedByMonsterID
              ,AllyStatusID
              ,MutationID
        from Object""",
    )

    db.execute_sqlite_sql(
        connection,
        """
        select DungeonVersion
              ,MaxDepth
              ,MinSeed
              ,MaxSeed
        from LoadMetadata""",
    )

    db.execute_sqlite_sql(
        connection,
        """
        select CategoryID, Value
        from Category""",
    )

    db.execute_sqlite_sql(
        connection,
        """
        select KindID, Value
        from Kind""",
    )

    db.execute_sqlite_sql(
        connection,
        """
        select RunicID, Value
        from Runic""",
    )

    db.execute_sqlite_sql(
        connection,
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
        from vObject""",
    )


class TestPopulateEnumTables:
    def test_populate_category(self, initialized_in_memory_db: DBService):
        cursor = db.execute_sqlite_sql(
            initialized_in_memory_db.connection,
            """
            select CategoryID, Value
            from Category""",
        )
        assert len(cursor.fetchall()) == len(misc_test_catalog.unique_categories)
        # assert al(Category[v[1]] == v[0] for v in cursor.fetchall())

    def test_populate_runic(self, initialized_in_memory_db: DBService):
        cursor = db.execute_sqlite_sql(
            initialized_in_memory_db.connection,
            """
            select RunicID, Value
            from Runic""",
        )
        assert len(cursor.fetchall()) == len(misc_test_catalog.unique_runics)
        # assert all(Runic[v[1]] == v[0] for v in cursor.fetchall())

    @pytest.mark.skip
    def test_populate_kind(self, initialized_in_memory_db: DBService):
        cursor = db.execute_sqlite_sql(
            initialized_in_memory_db.connection,
            """
            select KindID, Value
            from Kind""",
        )
        assert len(cursor.fetchall()) == len(misc_test_catalog.unique_kinds)
        # assert all(Runic[v[1]] == v[0] for v in cursor.fetchall())


def test_insert_single_catalog_object(initialized_in_memory_db: DBService):
    """Validate that when we insert 1 object, the Object table contains 1 row."""
    to_insert = [misc_test_objects[0]]
    db.insert_catalog_objects(
        initialized_in_memory_db.connection,
        to_insert,
        initialized_in_memory_db.structural_data_store,
    )
    select_count_cursor = db.execute_sqlite_sql(
        initialized_in_memory_db.connection, "select count(*) from Object"
    )
    assert select_count_cursor.fetchone()[0] == 1


def test_insert_multiple_catalog_objects(initialized_in_memory_db: DBService):
    """Validate that when we insert 5 objects, the Object table contains 5 rows."""
    db.insert_catalog_objects(
        initialized_in_memory_db.connection,
        misc_test_objects,
        initialized_in_memory_db.structural_data_store,
    )
    select_count_cursor = db.execute_sqlite_sql(
        initialized_in_memory_db.connection, "select count(*) from Object"
    )
    assert select_count_cursor.fetchone()[0] == len(misc_test_objects)


def test_insert_catalog_metadata(initialized_in_memory_db: DBService):
    """Validate that when insert catalog metadata, the LoadMetadata reflects it."""
    db.insert_catalog_metadata(initialized_in_memory_db.connection, misc_test_metadata)
    cursor = db.execute_sqlite_sql(
        initialized_in_memory_db.connection, "select * from LoadMetadata"
    )
    data = cursor.fetchall()
    assert len(data) == 1
    assert data == [("CE 1.9", 26, 1, 1)]
