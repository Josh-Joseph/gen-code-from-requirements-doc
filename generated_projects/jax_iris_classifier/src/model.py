import logging
from typing import Tuple

import jax
import jax.numpy as jnp
import numpy as np
from jax.experimental.optimizers import adam
from jax.experimental.stax import Dense, Relu, Softmax, serial

logger = logging.getLogger(__name__)

# This file defines the IrisClassifier class, which is a feed-forward neural network classifier for the iris dataset.

class IrisClassifier:
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.build_network()

    # Builds the neural network architecture and initializes the parameters and optimizer.
    def build_network(self) -> None:
        init_random_params, self.predict = serial(
            Dense(16),
            Relu,
            Dense(16),
            Relu,
            Dense(3),
            Softmax,
        )

        rng = jax.random.PRNGKey(0)
        _, self.params = init_random_params(rng, (-1, 4))

        self.opt_init, self.opt_update, self.get_params = adam(self.learning_rate)
        self.opt_state = self.opt_init(self.params)

    # Computes the loss for the given parameters and batch.
    def loss(self, params, batch) -> float:
        inputs, targets = batch
        preds = self.predict(params, inputs)
        return -jnp.mean(jnp.sum(targets * jnp.log(preds), axis=1))

    # Computes the accuracy for the given parameters and batch.
    def accuracy(self, params, batch) -> float:
        inputs, targets = batch
        target_class = jnp.argmax(targets, axis=1)
        predicted_class = jnp.argmax(self.predict(params, inputs), axis=1)
        return jnp.mean(predicted_class == target_class)

    # Performs one optimization step using the given parameters, optimizer state, and batch.
    def step(self, i, opt_state, batch) -> Tuple:
        params = self.get_params(opt_state)
        grad = jax.grad(self.loss)(params, batch)
        return self.opt_update(i, grad, opt_state)

    # One-hot encodes the given labels.
    def one_hot_encode_labels(self, labels: np.ndarray) -> np.ndarray:
        label_to_index = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
        labels = np.array([label_to_index[label] for label in labels])
        one_hot_labels = np.zeros((labels.size, labels.max() + 1))
        one_hot_labels[np.arange(labels.size), labels] = 1
        return one_hot_labels

    # Trains the classifier on the given features and labels for the specified number of epochs.
    def train(self, features: np.ndarray, labels: np.ndarray, epochs: int = 100) -> None:
        one_hot_labels = self.one_hot_encode_labels(labels)
        for epoch in range(epochs):
            self.opt_state = self.step(epoch, self.opt_state, (features, one_hot_labels))

            if epoch % 10 == 0:
                params = self.get_params(self.opt_state)
                train_loss = self.loss(params, (features, one_hot_labels))
                train_accuracy = self.accuracy(params, (features, one_hot_labels))
                logger.info(f"Epoch {epoch}: loss = {train_loss}, accuracy = {train_accuracy}")

    # Tests the classifier on the given features and labels and returns the accuracy.
    def test(self, features: np.ndarray, labels: np.ndarray) -> float:
        one_hot_labels = self.one_hot_encode_labels(labels)
        params = self.get_params(self.opt_state)
        test_accuracy = self.accuracy(params, (features, one_hot_labels))
        logger.info(f"Test accuracy: {test_accuracy}")
        return test_accuracy
