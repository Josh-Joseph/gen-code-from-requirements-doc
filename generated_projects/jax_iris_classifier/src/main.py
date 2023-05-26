import logging
from pathlib import Path
import numpy as np

from data import download_iris_data, split_data
from model import IrisClassifier


def main() -> None:
    # Set up logging
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Download the iris dataset
    logging.info("Downloading the iris dataset")
    features, labels = download_iris_data()

    # Split the dataset into training and testing sets
    logging.info("Splitting the dataset into train and test sets")
    train_features, train_labels, test_features, test_labels = split_data(features, labels)

    # Train the classifier
    logging.info("Training the classifier")
    classifier = IrisClassifier()
    classifier.train(train_features, train_labels)

    # Test the classifier
    logging.info("Testing the classifier")
    accuracy = classifier.test(test_features, test_labels)

    # Log the final accuracy
    logging.info(f"Final accuracy: {accuracy:.2f}")


if __name__ == "__main__":
    main()
