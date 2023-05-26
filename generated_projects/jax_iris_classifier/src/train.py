import logging
from pathlib import Path
import numpy as np
from jax import random, config
from src.data import download_iris_data, split_data
from src.model import IrisClassifier

config.update("jax_platform_name", "cpu")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def main() -> None:
    logging.info("Downloading iris dataset")
    features, labels = download_iris_data()

    logging.info("Splitting dataset into train and test sets")
    train_features, train_labels, test_features, test_labels = split_data(features, labels)

    logging.info("Training the classifier")
    classifier = IrisClassifier()
    classifier.build_network()
    classifier.train(train_features, train_labels)

    logging.info("Testing the classifier")
    accuracy = classifier.test(test_features, test_labels)
    logging.info(f"Final accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    main()
