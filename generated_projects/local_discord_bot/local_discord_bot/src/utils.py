from typing import Dict


def count_characters(text: str) -> Dict[str, int]:
    """
    Counts the occurrences of each character in the given text.
    
    Args:
        text (str): The input text to count characters in.
    
    Returns:
        Dict[str, int]: A dictionary mapping characters to their counts in the input text.
    """
    character_counts = {}
    for char in text:
        character_counts[char] = character_counts.get(char, 0) + 1
    return character_counts