import numpy as np
from src.data import download_iris_data, split_data


def test_download_iris_data() -> None:
    features, labels = download_iris_data()
    assert features.shape == (150, 4), "Features shape should be (150, 4)"
    assert labels.shape == (150,), "Labels shape should be (150,)"
    assert np.unique(labels).tolist() == [0, 1, 2], "Labels should have 3 unique values (0, 1, 2)"


def test_split_data() -> None:
    features = np.random.rand(150, 4)
    labels = np.array([0] * 50 + [1] * 50 + [2] * 50)
    train_features, train_labels, test_features, test_labels = split_data(features, labels)

    assert train_features.shape == (144, 4), "Train features shape should be (144, 4)"
    assert train_labels.shape == (144,), "Train labels shape should be (144,)"
    assert test_features.shape == (6, 4), "Test features shape should be (6, 4)"
    assert test_labels.shape == (6,), "Test labels shape should be (6,)"
    assert np.unique(test_labels).tolist() == [0, 1, 2], "Test labels should have 3 unique values (0, 1, 2)"
    assert np.all(test_labels == np.array([0, 0, 1, 1, 2, 2])), "Test labels should have 2 samples from each class"
