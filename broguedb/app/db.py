from collections.abc import Collection
import dataclasses
import logging
import sqlite3

from broguedb import fileutil
from broguedb.app.data import CatalogMetadata
from broguedb.app.data import CatalogObject
from broguedb.app.data import Category
from broguedb.app.data import Kind
from broguedb.app.data import Runic

_logger = logging.getLogger(__name__)


_enum_table_sources = (Category, Kind, Runic)


_insert_catalog_object_statement = (
    "insert into Object(Seed, Depth, Quantity, CategoryID, KindID, Enchantment, "
    "RunicID, VaultNumber, OpensVaultNumber, CarriedByMonsterName, AllyStatusName, "
    "MutationName) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
)
_insert_catalog_metadata_statement = (
    "insert into LoadMetadata(DungeonVersion, MaxDepth, MinSeed, MaxSeed) "
    "values (?, ?, ?, ?)"
)


def execute_sqlite_sql(
    connection: sqlite3.Connection, sql: str, parameters: Collection = None
) -> sqlite3.Cursor:

    _logger.debug(
        "sqlite execute: %s%s",
        sql,
        f"{' parameters: ' + str(parameters) if parameters is not None else ''}",
    )
    if parameters is not None:
        return connection.execute(sql, parameters)
    return connection.execute(sql)


def executemany_sqlite_sql(
    connection: sqlite3.Connection, sql: str, parameters: Collection[Collection]
) -> sqlite3.Cursor:

    _logger.debug("sqlite executemany (%d parameter sets): %s", len(parameters), sql)
    return connection.executemany(sql, parameters)


def set_up_fresh_db(connection: sqlite3.Connection) -> None:
    run_ddl(connection)
    populate_enum_tables(connection)


def run_ddl(connection: sqlite3.Connection) -> None:
    ddl_root = fileutil.get_path_relative_to_project_root("sql")
    ddl_directories = [ddl_root / "tables", ddl_root / "views"]
    _logger.info("Running DDL on new DB")
    for ddl_root in ddl_directories:
        for path in ddl_root.iterdir():
            if path.is_file():
                sql = path.read_text(encoding="utf-8")
                execute_sqlite_sql(connection, sql)


def populate_enum_tables(connection: sqlite3.Connection) -> None:
    insert_many_sql_template = "insert into {0} values (?, ?)"
    _logger.info("Populating enum tables in new DB")

    for enum_table_source in _enum_table_sources:
        insert_statement = insert_many_sql_template.format(enum_table_source.__name__)
        params = tuple((e.value, e.name) for e in enum_table_source)
        executemany_sqlite_sql(connection, insert_statement, params)


def insert_catalog_objects(
    connection: sqlite3.Connection, catalog_objects: Collection[CatalogObject]
) -> None:

    _logger.info("Persisting catalog objects")
    executemany_sqlite_sql(
        connection,
        _insert_catalog_object_statement,
        tuple(dataclasses.astuple(c) for c in catalog_objects),
    )
    _logger.info("Persisted %d catalog objects", len(catalog_objects))


def insert_catalog_metadata(
    connection: sqlite3.Connection, catalog_metadata: CatalogMetadata
) -> None:

    _logger.info("Persisting catalog metadata")
    execute_sqlite_sql(
        connection,
        _insert_catalog_metadata_statement,
        dataclasses.astuple(catalog_metadata),
    )
