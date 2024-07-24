import pytest
from src.patch_typings import patch_directory

def test_import() -> None:
    """
    Test if the patch_directory function can be imported correctly.
    """
    assert patch_directory is not None
