import numpy as np
from pathlib import Path
from typing import Tuple
import urllib.request


def download_iris_data() -> Tuple[np.ndarray, np.ndarray]:
    """Downloads the iris dataset and returns the features and labels as numpy arrays.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The features and labels as numpy arrays.
    """
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    file_path = Path("iris_data.csv")

    if not file_path.exists():
        urllib.request.urlretrieve(url, file_path)

    data = np.genfromtxt(file_path, delimiter=",", dtype=float, usecols=(0, 1, 2, 3, 4), encoding="ascii")
    features = data[:, :4]
    labels = data[:, 4]

    return features, labels


def split_data(features: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Splits the dataset into training and testing sets, where the test set is the last 2 data points from each class.

    Args:
        features (np.ndarray): The features of the dataset.
        labels (np.ndarray): The labels of the dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: The train_features, train_labels, test_features, and test_labels as numpy arrays.
    """
    unique_labels = np.unique(labels)
    train_features, train_labels, test_features, test_labels = [], [], [], []

    for label in unique_labels:
        label_indices = np.where(labels == label)[0]
        train_indices = label_indices[:-2]
        test_indices = label_indices[-2:]

        train_features.append(features[train_indices])
        train_labels.append(labels[train_indices])
        test_features.append(features[test_indices])
        test_labels.append(labels[test_indices])

    train_features = np.vstack(train_features)
    train_labels = np.hstack(train_labels)
    test_features = np.vstack(test_features)
    test_labels = np.hstack(test_labels)

    return train_features, train_labels, test_features, test_labels
