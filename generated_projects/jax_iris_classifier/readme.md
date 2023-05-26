# JAX IRIS Classifier

This project trains and tests a feed-forward neural network classifier built using JAX on the iris dataset. The classifier is run as a bash script that sets up a virtual environment, installs necessary requirements, downloads the data, splits the data into train and test sets, trains the classifier, tests the classifier, and exits the virtual environment.

## Setup and Usage Instructions

All commands should be run from the root folder of the codebase: `generated_projects/jax_iris_classifier`. To set up and run the classifier, execute the following command:

```bash
./set_up_and_run.sh
```

## Code Organization

```
generated_projects/
└── jax_iris_classifier/
    ├── src/
    │   ├── __init__.py
    │   ├── data.py
    │   ├── model.py
    │   └── main.py
    ├── tests/
    │   ├── test_data.py
    │   ├── test_model.py
    │   └── test_main.py
    ├── set_up_and_run.sh
    ├── readme.md
    ├── requirements.txt
    ├── LICENSE
    └── project_tech_spec.md
```

For more information about the code organization, dependencies, and individual file contents, please refer to the [technical specification document](project_tech_spec.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
