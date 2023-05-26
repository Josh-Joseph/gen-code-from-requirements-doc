import logging
import numpy as np
from pathlib import Path
from typing import Tuple
from urllib.request import urlretrieve

logger = logging.getLogger(__name__)

IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
IRIS_DATA_FILE = "iris.data"


def download_iris_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Downloads the iris dataset and returns the features and labels as numpy arrays.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The features and labels as numpy arrays.
    """
    if not Path(IRIS_DATA_FILE).is_file():
        logger.info("Downloading iris dataset")
        urlretrieve(IRIS_URL, IRIS_DATA_FILE)

    with open(IRIS_DATA_FILE, "r") as f:
        data = [line.strip().split(",") for line in f.readlines() if line.strip()]

    features = np.array([row[:-1] for row in data if len(row) > 0], dtype=np.float32)
    labels = np.array([row[-1] for row in data if len(row) > 0])

    return features, labels


def split_data(features: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the dataset into training and testing sets where the test set is the last 2 data points from each class.

    Args:
        features (np.ndarray): The features of the dataset.
        labels (np.ndarray): The labels of the dataset.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: The train_features, train_labels, test_features, and
        test_labels as numpy arrays.
    """
    unique_labels = np.unique(labels)
    train_features, train_labels, test_features, test_labels = [], [], [], []

    for label in unique_labels:
        label_indices = np.where(labels == label)[0]
        train_indices = label_indices[:-2]
        test_indices = label_indices[-2:]

        train_features.extend(features[train_indices])
        train_labels.extend(labels[train_indices])
        test_features.extend(features[test_indices])
        test_labels.extend(labels[test_indices])

    return (
        np.array(train_features, dtype=np.float32),
        np.array(train_labels),
        np.array(test_features, dtype=np.float32),
        np.array(test_labels),
    )

