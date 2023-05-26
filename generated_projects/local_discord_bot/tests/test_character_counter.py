# test_character_counter.py

import pytest
from collections import Counter
from src.character_counter import count_characters


@pytest.mark.parametrize("text, expected", [
    ("hello", {"h": 1, "e": 1, "l": 2, "o": 1}),
    ("", {}),
    ("aaabbbccc", {"a": 3, "b": 3, "c": 3}),
    ("123", {"1": 1, "2": 1, "3": 1}),
    ("AaBbCc", {"A": 1, "a": 1, "B": 1, "b": 1, "C": 1, "c": 1}),
])
def test_count_characters(text, expected):
    assert count_characters(text) == expected
