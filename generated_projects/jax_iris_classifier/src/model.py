import jax
import jax.numpy as jnp
from jax.experimental import optimizers
from typing import Tuple


class IrisClassifier:
    def __init__(self, learning_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.params = self._initialize_params()
        self.opt_init, self.opt_update, self.get_params = optimizers.adam(self.learning_rate)
        self.opt_state = self.opt_init(self.params)

    def _initialize_params(self) -> Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray]:
        key = jax.random.PRNGKey(0)
        key, layer1_key, layer2_key, output_key = jax.random.split(key, 4)

        layer1_weights = jax.random.normal(layer1_key, (4, 16))
        layer1_biases = jnp.zeros(16)

        layer2_weights = jax.random.normal(layer2_key, (16, 16))
        layer2_biases = jnp.zeros(16)

        output_weights = jax.random.normal(output_key, (16, 3))
        output_biases = jnp.zeros(3)

        return layer1_weights, layer1_biases, layer2_weights, layer2_biases, output_weights, output_biases

    @staticmethod
    @jax.jit
    def _relu(x: jnp.ndarray) -> jnp.ndarray:
        return jnp.maximum(0, x)

    @staticmethod
    @jax.jit
    def _softmax(x: jnp.ndarray) -> jnp.ndarray:
        return jnp.exp(x) / jnp.sum(jnp.exp(x), axis=-1, keepdims=True)

    @jax.jit
    def _forward_pass(self, params: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray], x: jnp.ndarray) -> jnp.ndarray:
        layer1_weights, layer1_biases, layer2_weights, layer2_biases, output_weights, output_biases = params

        layer1_output = self._relu(jnp.dot(x, layer1_weights) + layer1_biases)
        layer2_output = self._relu(jnp.dot(layer1_output, layer2_weights) + layer2_biases)
        output = self._softmax(jnp.dot(layer2_output, output_weights) + output_biases)

        return output

    @jax.jit
    def _loss(self, params: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray], x: jnp.ndarray, y: jnp.ndarray) -> jnp.ndarray:
        predictions = self._forward_pass(params, x)
        return -jnp.mean(jnp.sum(y * jnp.log(predictions), axis=-1))

    @jax.jit
    def _accuracy(self, params: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray], x: jnp.ndarray, y: jnp.ndarray) -> jnp.ndarray:
        predictions = self._forward_pass(params, x)
        return jnp.mean(jnp.argmax(predictions, axis=-1) == jnp.argmax(y, axis=-1))

    @jax.jit
    def _update(self, i: int, opt_state: optimizers.OptimizerState, x: jnp.ndarray, y: jnp.ndarray) -> Tuple[optimizers.OptimizerState, jnp.ndarray]:
        params = self.get_params(opt_state)
        loss, grads = jax.value_and_grad(self._loss)(params, x, y)
        return self.opt_update(i, grads, opt_state), loss

    def train(self, features: jnp.ndarray, labels: jnp.ndarray, epochs: int = 100) -> None:
        for epoch in range(epochs):
            self.opt_state, loss = self._update(epoch, self.opt_state, features, labels)
            if epoch % 10 == 0:
                params = self.get_params(self.opt_state)
                accuracy = self._accuracy(params, features, labels)
                print(f"Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

    def test(self, features: jnp.ndarray, labels: jnp.ndarray) -> float:
        params = self.get_params(self.opt_state)
        accuracy = self._accuracy(params, features, labels)
        return accuracy
