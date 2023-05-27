# JAX IRIS Classifier

This project trains and tests a feed-forward neural network classifier built using JAX on the iris dataset. The classifier is run as a bash script that sets up a virtual environment, installs necessary requirements, downloads the data, splits the data into train and test sets, trains the classifier, tests the classifier, and exits the virtual environment.

## Setup and Usage Instructions

1. Clone the repository and navigate to the `generated_projects/jax_iris_classifier` directory.
2. Ensure you have Python 3.7 or higher installed on your system.
3. Run the `set_up_and_run.sh` script from the command line:

```bash
./set_up_and_run.sh
```

This script will create a Python virtual environment, install the necessary requirements, download the iris dataset, split the dataset into training and testing sets, train the classifier, test the classifier, and exit the virtual environment.

## Project Structure

```
generated_projects/jax_iris_classifier
├── src
│   ├── __init__.py
│   ├── data.py
│   ├── model.py
│   └── train.py
├── tests
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_model.py
│   └── test_train.py
├── set_up_and_run.sh
├── requirements.txt
├── readme.md
└── LICENSE
```

For more information on the project's technical specifications, please refer to the [Technical Specification Document](./technical_specification.md).
