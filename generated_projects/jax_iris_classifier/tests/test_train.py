import logging
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from generated_projects.jax_iris_classifier.src import train

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class TestTrain(unittest.TestCase):
    @patch("generated_projects.jax_iris_classifier.src.train.download_iris_data")
    @patch("generated_projects.jax_iris_classifier.src.train.split_data")
    @patch("generated_projects.jax_iris_classifier.src.train.IrisClassifier")
    def test_main(self, mock_iris_classifier, mock_split_data, mock_download_iris_data):
        # Mock data
        features = np.random.rand(150, 4)
        labels = np.random.randint(0, 3, 150)
        train_features = features[:-6]
        train_labels = labels[:-6]
        test_features = features[-6:]
        test_labels = labels[-6:]

        # Mock functions and class
        mock_download_iris_data.return_value = (features, labels)
        mock_split_data.return_value = (train_features, train_labels, test_features, test_labels)
        mock_classifier_instance = MagicMock()
        mock_classifier_instance.test.return_value = 0.5
        mock_iris_classifier.return_value = mock_classifier_instance

        # Run main function
        train.main()

        # Check if functions and methods were called with correct arguments
        mock_download_iris_data.assert_called_once()
        mock_split_data.assert_called_once_with(features, labels)
        mock_iris_classifier.assert_called_once_with()
        mock_classifier_instance.build_network.assert_called_once()
        mock_classifier_instance.train.assert_called_once_with(train_features, train_labels)
        mock_classifier_instance.test.assert_called_once_with(test_features, test_labels)


if __name__ == "__main__":
    unittest.main()
