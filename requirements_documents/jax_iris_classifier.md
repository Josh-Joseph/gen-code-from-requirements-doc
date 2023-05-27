# JAX IRIS Classifier

## Overview

The purpose of this script is to train and test a feed-forward neural network classifier build using JAX on the iris dataset.

## Functional Requirements

- The classifier must be run as a bash script `<project_root>/set_up_and_run.sh` that does the following:
  - Creates a python virtual environment at `<project_root>/.venv`
  - Installs all of the necessary requirements into the virtual environment
  - Enters the virtual environment
  - Downloads the data
  - Splits the data into train and test sets
  - Trains the classifier
  - Tests the classifier
  - Exits the virtual environment
- Download the IRIS dataset
- Split the dataset into training and testing sets where the test set is the last 2 data points from each class
- Train a feed-forward neural network classifier using JAX
  - The network should have 2 hidden layers with 16 neurons each
  - The network should use the ReLU activation function
  - The network should use the softmax activation function for the output layer
  - The optimization should use the cross-entropy loss function
  - The optimization should use the Adam optimizer
  - The optimization should use a learning rate of 0.01
  - Run the optimization for 100 epochs
  - Log the loss and accuracy of the network at the `INFO` level every 10 epochs
- Test the classifier on the test set
  - Log the final accuracy of the classifier at the `INFO` level

## Non-functional Requirements

- Use the built-in `logging` module with module-level loggers formatted as `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE` where the datetime is in UTC.
  - Log all new occurrences of issues and actions taken by the bot at the `INFO` level.
- Use the MIT license for the project
- Run JAX on the CPU only 