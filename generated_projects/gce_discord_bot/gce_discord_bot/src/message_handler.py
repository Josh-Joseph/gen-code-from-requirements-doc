from typing import Dict, List

class MessageHandler:
    def __init__(self):
        self.subscribers: List[str] = []

    def subscribe_user(self, user_id: str) -> None:
        """Adds a user to the subscribers list.

        Args:
            user_id (str): The user's ID.
        """
        if user_id not in self.subscribers:
            self.subscribers.append(user_id)

    def unsubscribe_user(self, user_id: str) -> None:
        """Removes a user from the subscribers list.

        Args:
            user_id (str): The user's ID.
        """
        if user_id in self.subscribers:
            self.subscribers.remove(user_id)

    def process_message(self, message: str) -> Dict[str, int]:
        """Processes a message and returns a character count dictionary.

        Args:
            message (str): The message to process.

        Returns:
            Dict[str, int]: A dictionary with character counts.
        """
        char_count = {}
        for char in message:
            if char in char_count:
                char_count[char] += 1
            else:
                char_count[char] = 1
        return char_count