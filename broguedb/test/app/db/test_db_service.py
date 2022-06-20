import dataclasses
import sqlite3

import pytest

from broguedb.app import db
from broguedb.app.data import CatalogObject
from broguedb.app.db import DBService
from broguedb.test import csvtestdata

structural_data_tables = (
    "AllyStatus",
    "Category",
    "Kind",
    "Monster",
    "Mutation",
    "Runic",
)


@pytest.fixture
def in_memory_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(":memory:")


@pytest.fixture
def in_memory_db_service(in_memory_db_connection: sqlite3.Connection) -> DBService:
    return DBService(in_memory_db_connection, is_new_db=True)


@pytest.fixture
def prepared_in_memory_db_service(in_memory_db_service: DBService) -> DBService:
    in_memory_db_service.prepare_db()
    return in_memory_db_service


@pytest.fixture
def structurally_populated_in_memory_db_service(
    prepared_in_memory_db_service: DBService,
) -> DBService:

    prepared_in_memory_db_service.populate_structural_data(
        csvtestdata.misc_csv_file_catalog
    )
    return prepared_in_memory_db_service


class TestPrepareDB:
    @pytest.mark.parametrize("table_name", structural_data_tables)
    def test_structural_data_tables(
        self, prepared_in_memory_db_service: DBService, table_name: str
    ):

        query = f"select {table_name}ID, Value from {table_name}"
        db.execute_sqlite_sql(prepared_in_memory_db_service.connection, query)

    def test_object_table(self, prepared_in_memory_db_service: DBService):
        db.execute_sqlite_sql(
            prepared_in_memory_db_service.connection, db.query_for_all_object_columns
        )

    def test_load_metadata(self, prepared_in_memory_db_service: DBService):
        db.execute_sqlite_sql(
            prepared_in_memory_db_service.connection,
            db.query_for_all_load_metadata_columns,
        )

    def test_vobject_view(self, prepared_in_memory_db_service: DBService):
        db.execute_sqlite_sql(
            prepared_in_memory_db_service.connection, db.query_for_all_vobject_columns
        )


def test_insert_catalog_metadata(prepared_in_memory_db_service: DBService):
    metadata = csvtestdata.misc_csv_file_catalog_metadata
    prepared_in_memory_db_service.insert_catalog_metadata(metadata)
    cursor = db.execute_sqlite_sql(
        prepared_in_memory_db_service.connection, db.query_for_all_load_metadata_columns
    )
    assert cursor.fetchall()[0] == dataclasses.astuple(metadata)


class TestInsertCatalogObjects:
    @pytest.mark.parametrize(
        "catalog_object", csvtestdata.misc_csv_file_catalog_objects
    )
    def test_insert_single_object(
        self,
        structurally_populated_in_memory_db_service: DBService,
        catalog_object: CatalogObject,
    ):

        structurally_populated_in_memory_db_service.insert_catalog_objects(
            [catalog_object]
        )
