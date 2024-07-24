# Path: C:\AutoNoCode\tests\test_literal_import.py

from typing import Literal


def test_literal() -> None:
    test_value: Literal["test"] = "test"
    assert test_value == "test"
