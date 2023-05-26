```python
import numpy as np
from pathlib import Path
from src.data import download_iris_data, split_data

def test_download_iris_data():
    features, labels = download_iris_data()
    assert isinstance(features, np.ndarray), "Features should be a numpy array"
    assert isinstance(labels, np.ndarray), "Labels should be a numpy array"
    assert features.shape == (150, 4), "Features should have shape (150, 4)"
    assert labels.shape == (150,), "Labels should have shape (150,)"

def test_split_data():
    features = np.random.rand(150, 4)
    labels = np.array([0] * 50 + [1] * 50 + [2] * 50)
    train_features, train_labels, test_features, test_labels = split_data(features, labels)

    assert isinstance(train_features, np.ndarray), "Train features should be a numpy array"
    assert isinstance(train_labels, np.ndarray), "Train labels should be a numpy array"
    assert isinstance(test_features, np.ndarray), "Test features should be a numpy array"
    assert isinstance(test_labels, np.ndarray), "Test labels should be a numpy array"

    assert train_features.shape == (144, 4), "Train features should have shape (144, 4)"
    assert train_labels.shape == (144,), "Train labels should have shape (144,)"
    assert test_features.shape == (6, 4), "Test features should have shape (6, 4)"
    assert test_labels.shape == (6,), "Test labels should have shape (6,)"

    assert np.all(test_labels == [0, 0, 1, 1, 2, 2]), "Test labels should have 2 samples from each class"
```
