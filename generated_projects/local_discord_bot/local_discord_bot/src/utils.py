from typing import Dict


def count_characters(message: str) -> Dict[str, int]:
    """
    Counts the occurrences of each character in the given message.
    
    Args:
        message (str): The message to count characters in.
    
    Returns:
        Dict[str, int]: A dictionary mapping characters to their counts.
    """
    character_counts = {}
    for char in message:
        character_counts[char] = character_counts.get(char, 0) + 1
    return character_counts