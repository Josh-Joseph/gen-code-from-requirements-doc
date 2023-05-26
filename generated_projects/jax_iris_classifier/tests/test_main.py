import logging
import unittest
from unittest.mock import MagicMock, patch

from src import main, data, model


class TestMain(unittest.TestCase):

    @patch("src.main.logging")
    @patch("src.main.data")
    @patch("src.main.model")
    def test_main(self, mock_model, mock_data, mock_logging):
        # Set up mock objects
        mock_data.download_iris_data.return_value = (
            MagicMock(spec=data.np.ndarray),
            MagicMock(spec=data.np.ndarray),
        )
        mock_data.split_data.return_value = (
            MagicMock(spec=data.np.ndarray),
            MagicMock(spec=data.np.ndarray),
            MagicMock(spec=data.np.ndarray),
            MagicMock(spec=data.np.ndarray),
        )
        mock_classifier = MagicMock(spec=model.IrisClassifier)
        mock_model.IrisClassifier.return_value = mock_classifier
        mock_classifier.test.return_value = 0.75

        # Run the main function
        main.main()

        # Check that the functions were called with the correct arguments
        mock_data.download_iris_data.assert_called_once()
        mock_data.split_data.assert_called_once_with(
            mock_data.download_iris_data.return_value[0],
            mock_data.download_iris_data.return_value[1],
        )
        mock_model.IrisClassifier.assert_called_once_with(learning_rate=0.01)
        mock_classifier.train.assert_called_once_with(
            mock_data.split_data.return_value[0],
            mock_data.split_data.return_value[1],
            epochs=100,
        )
        mock_classifier.test.assert_called_once_with(
            mock_data.split_data.return_value[2],
            mock_data.split_data.return_value[3],
        )
        mock_logging.info.assert_called_with("Final accuracy: 0.75")


if __name__ == "__main__":
    unittest.main()
