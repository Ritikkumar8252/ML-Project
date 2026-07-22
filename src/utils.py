# Used to work with files and folders
import os

# Used to get system information (helps in custom error handling)
import sys

# NumPy library (not used in this file, can be removed if unnecessary)
import numpy as np

# Pandas library (not used in this file, can be removed if unnecessary)
import pandas as pd

# Dill library (not used here, pickle is used instead)


# Used to save and load Python objects like models
import pickle

# Used to calculate the R² score for regression models
from sklearn.metrics import r2_score

# Used to find the best hyperparameters automatically
from sklearn.model_selection import GridSearchCV

# Import our custom exception class
from src.exception import CustomException


# =====================================================
# Function to save any Python object (model, pipeline, etc.)
# =====================================================
def save_object(file_path, obj):
    try:
        # Get only the folder path from the complete file path
        # Example:
        # file_path = "artifacts/model.pkl"
        # dir_path = "artifacts"
        dir_path = os.path.dirname(file_path)

        # Create the folder if it does not already exist
        os.makedirs(dir_path, exist_ok=True)

        # Open the file in binary write mode ("wb")
        with open(file_path, "wb") as file_obj:

            # Save the object into the file
            pickle.dump(obj, file_obj)

    except Exception as e:
        # Raise custom error if something goes wrong
        raise CustomException(e, sys)


# =====================================================
# Function to train and evaluate multiple ML models
# =====================================================
def evaluate_models(X_train, y_train, X_test, y_test, models, param):

    try:

        # Dictionary to store model names and their test scores
        report = {}

        # Loop through every model
        for i in range(len(list(models))):

            # Get the current model
            model = list(models.values())[i]

            # Get hyperparameters for the current model
            para = param[list(models.keys())[i]]

            # Create GridSearchCV object
            # It tries different parameter combinations
            gs = GridSearchCV(model, para, cv=3)

            # Train GridSearchCV on training data
            gs.fit(X_train, y_train)

            # Update the model with the best parameters found
            model.set_params(**gs.best_params_)

            # Train the model again using the best parameters
            model.fit(X_train, y_train)

            # Predict values for training data
            y_train_pred = model.predict(X_train)

            # Predict values for testing data
            y_test_pred = model.predict(X_test)

            # Calculate R² score on training data
            train_model_score = r2_score(y_train, y_train_pred)

            # Calculate R² score on testing data
            test_model_score = r2_score(y_test, y_test_pred)

            # Save only the test score in the report dictionary
            report[list(models.keys())[i]] = test_model_score

        # Return scores of all models
        return report

    except Exception as e:
        # Raise custom error if anything fails
        raise CustomException(e, sys)


# =====================================================
# Function to load a saved model or pipeline
# =====================================================
def load_object(file_path):

    try:

        # Open the file in binary read mode ("rb")
        with open(file_path, "rb") as file_obj:

            # Read and return the saved object
            return pickle.load(file_obj)

    except Exception as e:
        # Raise custom error if loading fails
        raise CustomException(e, sys) 