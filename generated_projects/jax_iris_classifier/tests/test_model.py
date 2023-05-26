import unittest
from typing import Tuple
import numpy as np
from jax import random
from src.model import IrisClassifier

class TestIrisClassifier(unittest.TestCase):

    def test_iris_classifier_initialization(self):
        # Test the initialization of the classifier
        classifier = IrisClassifier(learning_rate=0.01)
        self.assertEqual(classifier.learning_rate, 0.01)

    def test_iris_classifier_build_network(self):
        # Test the network building process
        classifier = IrisClassifier(learning_rate=0.01)
        classifier.build_network()
        self.assertIsNotNone(classifier.network)

    def test_iris_classifier_train(self):
        # Test the training process
        classifier = IrisClassifier(learning_rate=0.01)
        classifier.build_network()

        # Create dummy data for training
        rng = random.PRNGKey(0)
        features = random.normal(rng, (150, 4))
        labels = np.random.randint(0, 3, size=(150,))

        # Train the classifier
        classifier.train(features, labels, epochs=100)

    def test_iris_classifier_test(self):
        # Test the testing process
        classifier = IrisClassifier(learning_rate=0.01)
        classifier.build_network()

        # Create dummy data for testing
        rng = random.PRNGKey(0)
        features = random.normal(rng, (150, 4))
        labels = np.random.randint(0, 3, size=(150,))

        # Train the classifier
        classifier.train(features, labels, epochs=100)

        # Test the classifier
        accuracy = classifier.test(features, labels)

        # Check if the accuracy is within a reasonable range
        self.assertTrue(0 <= accuracy <= 1)

if __name__ == '__main__':
    unittest.main()
