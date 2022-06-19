import pathlib
import sqlite3

from click.testing import CliRunner
import pytest

from broguedb import fileutil
from broguedb.app import db
from broguedb.app.main import load_catalog


def test_db_parameter_parameters_rejected(tmp_path: pathlib.Path):
    tmp_file = tmp_path / "abc"
    tmp_file.touch()
    runner = CliRunner()
    result = runner.invoke(
        load_catalog,
        [
            "--csv-path",
            str(tmp_file),
        ],
    )
    assert result.exit_code == 1, result.stdout


def test_empty_catalog(tmp_path: pathlib.Path):
    create_db_at = str(tmp_path / "tmp.db")
    empty_catalog_path = fileutil.get_path_relative_to_project_root(
        "test-catalogs/catalog-empty.csv"
    )
    runner = CliRunner()
    result = runner.invoke(
        load_catalog,
        ["--csv-path", str(empty_catalog_path), "--new-db", str(create_db_at)],
    )
    assert isinstance(result.exception, SystemExit), result.stdout
    assert result.exit_code == 2, result.stdout


def test_misc_catalog_success(tmp_path: pathlib.Path):
    create_db_at = str(tmp_path / "tmp.db")
    misc_catalog_path = fileutil.get_path_relative_to_project_root(
        "test-catalogs/catalog-misc.csv"
    )
    runner = CliRunner()
    result = runner.invoke(
        load_catalog,
        ["--csv-path", str(misc_catalog_path), "--new-db", str(create_db_at)],
    )
    assert result.exit_code == 0, result.stdout


@pytest.mark.skip
def test_misc_catalog_metadata_persistence(tmp_path: pathlib.Path):
    create_db_at = str(tmp_path / "tmp.db")
    misc_catalog_path = fileutil.get_path_relative_to_project_root(
        "test-catalogs/catalog-misc.csv"
    )
    runner = CliRunner()
    result = runner.invoke(
        load_catalog,
        ["--csv-path", str(misc_catalog_path), "--new-db", str(create_db_at)],
    )
    assert result.exit_code == 0, result.stdout

    db_connection = sqlite3.connect(create_db_at)
    cursor = db.execute_sqlite_sql(db_connection, "select * from LoadMetadata")
    data = cursor.fetchall()
    assert len(data) == 1
    assert data == [("CE 1.9", 26, 1, 1)]


@pytest.mark.skip
def test_misc_catalog_object_persistence(tmp_path: pathlib.Path):
    create_db_at = str(tmp_path / "tmp.db")
    misc_catalog_path = fileutil.get_path_relative_to_project_root(
        "test-catalogs/catalog-misc.csv"
    )
    runner = CliRunner()
    result = runner.invoke(
        load_catalog,
        ["--csv-path", str(misc_catalog_path), "--new-db", str(create_db_at)],
    )
    assert result.exit_code == 0, result.stdout

    db_connection = sqlite3.connect(create_db_at)
    cursor = db.execute_sqlite_sql(db_connection, "select * from Object")
    data = cursor.fetchall()
    assert len(data) == 5
