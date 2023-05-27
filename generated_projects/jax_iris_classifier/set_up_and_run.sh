#!/bin/bash

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Download and split the iris dataset
echo "Downloading and splitting the iris dataset..."
python -c "from src.data import download_iris_data, split_data; features, labels = download_iris_data(); train_features, train_labels, test_features, test_labels = split_data(features, labels)"

# Train and test the classifier
echo "Training and testing the classifier..."
python -c "from src.train import main; main()"

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate
