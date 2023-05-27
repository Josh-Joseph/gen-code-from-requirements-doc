import unittest
from src.character_counter import count_characters


class TestCharacterCounter(unittest.TestCase):

    def test_count_characters(self):
        test_cases = [
            ("hello", {"h": 1, "e": 1, "l": 2, "o": 1}),
            ("", {}),
            ("aaa", {"a": 3}),
            ("AaBbCc", {"A": 1, "a": 1, "B": 1, "b": 1, "C": 1, "c": 1}),
            ("123", {"1": 1, "2": 1, "3": 1}),
        ]

        for message, expected_output in test_cases:
            with self.subTest(message=message, expected_output=expected_output):
                self.assertEqual(count_characters(message), expected_output)


if __name__ == "__main__":
    unittest.main()
