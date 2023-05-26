import numpy as np
import jax
import jax.numpy as jnp
from jax import random
from jax.experimental import optimizers

from src.model import IrisClassifier


def test_iris_classifier_train():
    # Create a random dataset for testing
    rng = random.PRNGKey(0)
    features = random.normal(rng, (100, 4))
    labels = jnp.array([0, 1, 2] * 33 + [0])

    # Initialize the classifier and train it
    classifier = IrisClassifier()
    classifier.train(features, labels)

    # Check if the classifier's parameters have been updated
    updated_params = classifier.params
    for layer_params in updated_params:
        for param in layer_params:
            assert not jnp.allclose(param, 0.0)


def test_iris_classifier_test():
    # Create a random dataset for testing
    rng = random.PRNGKey(0)
    features = random.normal(rng, (100, 4))
    labels = jnp.array([0, 1, 2] * 33 + [0])

    # Initialize the classifier and train it
    classifier = IrisClassifier()
    classifier.train(features, labels)

    # Test the classifier and check the accuracy
    accuracy = classifier.test(features, labels)
    assert isinstance(accuracy, float)
    assert 0 <= accuracy <= 1
