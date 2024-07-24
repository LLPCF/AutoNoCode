# Path: C:\AutoNoCode\tests\test_literal.py

from typing import Literal


def test_literal_function() -> None:
    test_value: Literal["test"] = "test"
    assert test_value == "test"
