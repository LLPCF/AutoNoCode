"""
Testes para o módulo patch_typings.
"""

from typing import Union

import pytest
from _pytest.python_api import RaisesContext

from src.patch_typings import patch_directory


@pytest.mark.parametrize(
    "src, backup, expected",
    [
        ("src", "src_backup", True),
        ("nonexistent", "src_backup", pytest.raises(FileNotFoundError)),
        ("src", "", pytest.raises(ValueError)),
        ("src", "backup", True),
    ],
)
def test_patch_directory_parametrized(
    src: str,
    backup: str,
    expected: Union[RaisesContext[FileNotFoundError], RaisesContext[ValueError], bool],
) -> None:
    if isinstance(expected, RaisesContext):
        with expected:
            patch_directory(src, backup)
    else:
        result = patch_directory(src, backup)
        assert result is expected
