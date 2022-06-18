import pathlib

import pytest

from broguedb.app import main


def test_resolve_db_params_both_params_non_null(tmp_path: pathlib.Path):
    with pytest.raises(SystemExit):
        main.resolve_db_parameters(tmp_path, tmp_path)


def test_resolve_db_params_both_params_null():
    with pytest.raises(SystemExit):
        main.resolve_db_parameters(None, None)


def test_resolve_db_params_valid_update_param_provided(tmp_path: pathlib.Path):
    db_path = tmp_path / "db.db"
    db_path.touch()
    assert main.resolve_db_parameters(None, db_path) == db_path


def test_resolve_db_params_valid_create_param_provided(tmp_path: pathlib.Path):
    db_path = tmp_path / "db.db"
    assert main.resolve_db_parameters(db_path, None) == db_path


def test_resolve_db_params_create_param_is_not_in_dir(tmp_path: pathlib.Path):
    db_path = tmp_path / "a" / "b"
    with pytest.raises(SystemExit):
        main.resolve_db_parameters(db_path, None)


def test_resolve_db_params_param_is_directory(tmp_path: pathlib.Path):
    with pytest.raises(SystemExit):
        main.resolve_db_parameters(None, tmp_path)


def test_resolve_db_params_param_does_not_exist(tmp_path: pathlib.Path):
    db_path = tmp_path / "x"
    with pytest.raises(SystemExit):
        main.resolve_db_parameters(None, db_path)
