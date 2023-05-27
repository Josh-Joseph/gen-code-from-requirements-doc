from typing import Dict


def count_characters(message: str) -> Dict[str, int]:
    """
    Count the occurrences of each character in the given message.

    Args:
        message (str): The message to count characters in.

    Returns:
        Dict[str, int]: A dictionary mapping characters to their counts.
    """
    character_counts = {}

    for char in message:
        if char in character_counts:
            character_counts[char] += 1
        else:
            character_counts[char] = 1

    return character_counts
