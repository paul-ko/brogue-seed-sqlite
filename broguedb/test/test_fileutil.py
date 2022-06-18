from pathlib import Path

import pytest

from broguedb import fileutil


def test_absolute_str_path():
    with pytest.raises(ValueError):
        fileutil.get_path_relative_to_project_root("C:/abc")


def test_absolute_pathlib_path():
    with pytest.raises(ValueError):
        fileutil.get_path_relative_to_project_root(Path("C:/abc"))


def test_relative_str_path():
    path = fileutil.get_path_relative_to_project_root("test-catalogs/catalog-misc.csv")
    assert path.exists()
    assert path.is_file()


def test_relative_pathlib_path():
    path = fileutil.get_path_relative_to_project_root(
        Path("test-catalogs/catalog-misc.csv")
    )
    assert path.exists()
    assert path.is_file()
