from collections import Counter
from typing import Dict


def count_characters(text: str) -> Dict[str, int]:
    """
    Counts the occurrences of each character in the given text and returns a dictionary
    with the character as the key and the count as the value.

    Args:
        text (str): The input text to count characters in.

    Returns:
        Dict[str, int]: A dictionary with characters as keys and their counts as values.
    """
    return dict(Counter(text))
