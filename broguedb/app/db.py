from collections.abc import Collection
import dataclasses
from dataclasses import dataclass
import logging
import sqlite3
from types import MappingProxyType
from typing import Optional

from broguedb import fileutil
from broguedb.app.data import CatalogMetadata
from broguedb.app.data import CatalogObject
from broguedb.app.readcsv import Catalog

_logger = logging.getLogger(__name__)


# Object table
_object_table_columns = (
    "Seed",
    "Depth",
    "Quantity",
    "CategoryID",
    "KindID",
    "Enchantment",
    "RunicID",
    "VaultNumber",
    "OpensVaultNumber",
    "CarriedByMonsterID",
    "AllyStatusID",
    "MutationID",
)
_joined_object_columns = ", ".join(_object_table_columns)
_insert_catalog_object_statement = (
    f"insert into Object({_joined_object_columns}) "
    f"values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
)
query_for_all_object_columns = f"select {_joined_object_columns} from Object"

# vObjectView
_vobject_view_columns = (
    "Seed",
    "Depth",
    "Quantity",
    "Category",
    "Kind",
    "Enchantment",
    "Runic",
    "VaultNumber",
    "OpensVaultNumber",
    "CarriedByMonsterName",
    "AllyStatusName",
    "MutationName",
)
_joined_vobject_columns = ", ".join(_vobject_view_columns)
query_for_all_vobject_columns = f"select {_joined_vobject_columns} from vObject"

# LoadMetadata table
_load_metadata_table_columns = ("DungeonVersion", "MaxDepth", "MinSeed", "MaxSeed")
_joined_load_metadata_columns = ", ".join(_load_metadata_table_columns)
_insert_catalog_metadata_statement = (
    f"insert into LoadMetadata({_joined_load_metadata_columns}) values (?, ?, ?, ?)"
)
query_for_all_load_metadata_columns = (
    f"select {_joined_load_metadata_columns} from LoadMetadata"
)

# DDL directories
_ddl_root = fileutil.get_path_relative_to_project_root("sql")
_ddl_directories = [_ddl_root / "tables", _ddl_root / "views"]


@dataclass(frozen=True)
class StructuralDataStore:
    categories: MappingProxyType[str, int]
    kinds: MappingProxyType[str, int]
    runics: MappingProxyType[str, int]
    monsters: MappingProxyType[str, int]
    ally_statuses: MappingProxyType[str, int]
    mutations: MappingProxyType[str, int]

    def generate_parameters_for_catalog_object(
        self, catalog_object: CatalogObject
    ) -> tuple:

        runic_id = (
            None if catalog_object.runic is None else self.runics[catalog_object.runic]
        )
        carried_by_monster_id = (
            None
            if catalog_object.carried_by_monster_name is None
            else self.monsters[catalog_object.carried_by_monster_name]
        )
        ally_status_id = (
            None
            if catalog_object.ally_status_name is None
            else self.ally_statuses[catalog_object.ally_status_name]
        )
        mutation_id = (
            None
            if catalog_object.mutation_name is None
            else self.mutations[catalog_object.mutation_name]
        )
        return (
            catalog_object.seed,
            catalog_object.depth,
            catalog_object.quantity,
            self.categories[catalog_object.category],
            self.kinds[catalog_object.kind],
            catalog_object.enchantment,
            runic_id,
            catalog_object.vault_number,
            catalog_object.opens_vault,
            carried_by_monster_id,
            ally_status_id,
            mutation_id,
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


class DBService:
    def __init__(self, connection: sqlite3.Connection, is_new_db: bool):
        self.connection = connection
        self.is_new_db = is_new_db
        self.structural_data_store: Optional[StructuralDataStore] = None

    def prepare_db(self):
        if self.is_new_db:
            with self.connection as connection:
                _logger.info("Running DDL on new DB")
                for ddl_root in _ddl_directories:
                    for path in ddl_root.iterdir():
                        if path.is_file():
                            sql = path.read_text(encoding="utf-8")
                            execute_sqlite_sql(connection, sql)

    def populate_structural_data(self, catalog: Catalog) -> None:
        categories = populate_structural_data_table(
            self.connection, "Category", catalog.unique_categories
        )
        kinds = populate_structural_data_table(
            self.connection, "Kind", catalog.unique_kinds
        )
        runics = populate_structural_data_table(
            self.connection, "Runic", catalog.unique_runics
        )
        monsters = populate_structural_data_table(
            self.connection, "Monster", catalog.unique_carried_by_monster_names
        )
        ally_statuses = populate_structural_data_table(
            self.connection, "AllyStatus", catalog.unique_ally_status_names
        )
        mutations = populate_structural_data_table(
            self.connection, "Mutation", catalog.unique_mutation_names
        )
        self.structural_data_store = StructuralDataStore(
            MappingProxyType(categories),
            MappingProxyType(kinds),
            MappingProxyType(runics),
            MappingProxyType(monsters),
            MappingProxyType(ally_statuses),
            MappingProxyType(mutations),
        )

    def insert_catalog_metadata(self, catalog_metadata: CatalogMetadata) -> None:
        with self.connection as connection:
            insert_catalog_metadata(connection, catalog_metadata)

    def insert_catalog_objects(
        self, catalog_objects: Collection[CatalogObject]
    ) -> None:

        if self.structural_data_store is None:
            raise ValueError(
                "Cannot persist catalog objects before populating structural data"
            )
        with self.connection as connection:
            insert_catalog_objects(
                connection, catalog_objects, self.structural_data_store
            )


def populate_structural_data_table(
    connection: sqlite3.Connection,
    name: str,
    values: Collection[str],
):

    assert name in (
        "Category",
        "Kind",
        "Monster",
        "AllyStatus",
        "Mutation",
        "Runic",
    )
    retrieval_query = f"select * from {name}"
    retrieval_cursor = execute_sqlite_sql(connection, retrieval_query)
    existing_values = {r[1] for r in retrieval_cursor.fetchall()}
    to_persist = {v for v in values if v not in existing_values}

    if len(to_persist):
        with connection:
            insert_statement = f"insert into {name}(Value) values (?)"
            parameters = [[v] for v in to_persist]
            executemany_sqlite_sql(connection, insert_statement, parameters)

    retrieval_cursor = execute_sqlite_sql(connection, retrieval_query)
    return {r[1]: r[0] for r in retrieval_cursor.fetchall()}


def insert_catalog_objects(
    connection: sqlite3.Connection,
    catalog_objects: Collection[CatalogObject],
    structural_data_score: StructuralDataStore,
) -> None:

    _logger.info("Persisting catalog objects")
    connection.execute("pragma foreign_keys = on")
    executemany_sqlite_sql(
        connection,
        _insert_catalog_object_statement,
        list(
            structural_data_score.generate_parameters_for_catalog_object(c)
            for c in catalog_objects
        ),
    )
    _logger.info("Persisted %d catalog objects", len(catalog_objects))


def insert_catalog_metadata(
    connection: sqlite3.Connection, catalog_metadata: CatalogMetadata
) -> None:

    _logger.info("Persisting catalog metadata")
    execute_sqlite_sql(
        connection,
        _insert_catalog_metadata_statement,
        dataclasses.astuple(catalog_metadata)[:4],
    )
