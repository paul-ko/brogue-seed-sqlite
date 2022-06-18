import logging
import pathlib
import sqlite3
import sys
from typing import Optional

import click

from broguedb.app import db
from broguedb.app import readcsv

_logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--create-db-at",
    "--new-db",
    type=click.Path(
        file_okay=False,
        dir_okay=False,
        writable=True,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--update-db-at",
    "--current-db",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--csv-path",
    "--csv",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=pathlib.Path,
    ),
    required=True,
)
def load_catalog(
    csv_path,
    create_db_at,
    update_db_at,
) -> None:

    db_path = resolve_db_parameters(create_db_at, update_db_at)

    try:
        catalog = readcsv.read_file(csv_path)
    except readcsv.EmptyCatalogError:
        _logger.error("No data in catalog")
        sys.exit(2)

    with sqlite3.connect(db_path) as db_connection:
        if create_db_at is not None:
            db.set_up_fresh_db(db_connection)
        db.insert_catalog_metadata(db_connection, catalog.catalog_metadata)
        db.insert_catalog_objects(db_connection, catalog.catalog_objects)


def resolve_db_parameters(
    create_db_at: Optional[pathlib.Path], update_db_at: Optional[pathlib.Path]
) -> pathlib.Path:

    if create_db_at is not None:
        if update_db_at is not None:
            _logger.error("Cannot specify two DBs")
            sys.exit(1)
        if not create_db_at.parent.is_dir():
            _logger.error(
                f"Cannot create a DB at {create_db_at.absolute()} because it is not in "
                f"an existing directory"
            )
            sys.exit(1)
        _logger.info("Creating a DB at %s", create_db_at.absolute())
        return create_db_at

    if update_db_at is not None:
        if not update_db_at.is_file():
            _logger.error(f"No DB exists at {update_db_at.absolute()}")
            sys.exit(1)
        _logger.info("Updating the DB at %s", update_db_at.absolute())
        return update_db_at

    _logger.error("Must specify a DB to create or update")
    sys.exit(1)


if __name__ == "__main__":
    load_catalog()  # pragma: no cover
