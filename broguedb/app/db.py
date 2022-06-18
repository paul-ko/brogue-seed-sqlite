from collections.abc import Collection
import dataclasses
import logging
import sqlite3

from broguedb import fileutil
from broguedb.app.data import CatalogObject

_logger = logging.getLogger(__name__)
_insert_catalog_object_statement = (
    "insert into Object(Seed, Depth, Quantity, Category, Kind, Enchantment, Runic, "
    "VaultNumber, OpensVaultNumber, CarriedByMonsterName, AllyStatusName, "
    "MutationName) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
)


def execute_sqlite_sql(
    connection: sqlite3.Connection, sql: str, parameters: Collection = None
) -> sqlite3.Cursor:

    _logger.debug(
        f"sqlite execute: {sql}"
        f"{' parameters: ' + str(parameters) if parameters is not None else ''}"
    )
    if parameters is not None:
        return connection.execute(sql, parameters)
    return connection.execute(sql)


def set_up_fresh_db(connection: sqlite3.Connection) -> None:
    ddl_root = fileutil.get_path_relative_to_project_root("sql")
    ddl_directories = [ddl_root / "tables"]
    for ddl_root in ddl_directories:
        for path in ddl_root.iterdir():
            if path.is_file():
                sql = path.read_text(encoding="utf-8")
                execute_sqlite_sql(connection, sql)


def insert_catalog_objects(
    connect: sqlite3.Connection, catalog_objects: Collection[CatalogObject]
) -> None:

    connect.executemany(
        _insert_catalog_object_statement,
        tuple(dataclasses.astuple(c) for c in catalog_objects),
    )
