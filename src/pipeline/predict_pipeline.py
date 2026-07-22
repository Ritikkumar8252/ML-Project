# ==========================================================
# Prediction Pipeline
#
# Why do we need this file?
#
# During training, we save:
#
# 1. model.pkl          -> Trained Machine Learning Model
# 2. preprocessor.pkl   -> Preprocessing Pipeline
#
# When a user enters new data,
# this file loads both saved files,
# preprocesses the input,
# and predicts the result.
#
# Flow
#
# User Input
#      │
#      ▼
# CustomData
#      │
#      ▼
# Pandas DataFrame
#      │
#      ▼
# PredictPipeline
#      │
#      ├── Load preprocessor.pkl
#      ├── Transform Input
#      ├── Load model.pkl
#      ├── Predict
#      └── Return Prediction
#
# ==========================================================

# Used to access system information.
# Why?
# It is passed to CustomException so that
# file name and line number can be shown if an error occurs.
import sys

# Used to create file paths.
# Why?
# os.path.join() creates paths that work
# on Windows, Linux and macOS.
import os

# Pandas is used to create DataFrames.
# Why?
# The preprocessing pipeline expects input
# in DataFrame format.
import pandas as pd

# Custom exception provides detailed error messages.
from src.exception import CustomException

# load_object() loads saved pickle files.
#
# Why?
#
# We use it to load:
#
# model.pkl
# preprocessor.pkl
#
# instead of training again.
from src.utils import load_object


# ==========================================================
# Prediction Pipeline Class
#
# Why?
#
# This class performs the complete prediction process.
#
# Responsibilities:
#
# ✔ Load model
# ✔ Load preprocessor
# ✔ Transform input
# ✔ Predict output
#
# ==========================================================
class PredictPipeline:

    # Constructor
    #
    # No initialization is required now,
    # so we simply use pass.
    def __init__(self):
        pass

    # ======================================================
    # Predict Function
    #
    # Why?
    #
    # This function predicts the output
    # for new user input.
    #
    # Steps:
    #
    # Load Model
    # ↓
    # Load Preprocessor
    # ↓
    # Transform Data
    # ↓
    # Predict
    #
    # ======================================================
    def predict(self, features):

        try:

            # Path of saved ML model.
            model_path = os.path.join(
                "artifacts",
                "model.pkl"
            )

            # Path of saved preprocessing pipeline.
            preprocessor_path = os.path.join(
                "artifacts",
                "preprocessor.pkl"
            )

            print("Before Loading")

            # Load trained model.
            #
            # Why?
            #
            # Instead of training every time,
            # we load the already-trained model.
            model = load_object(
                file_path=model_path
            )

            # Load preprocessing pipeline.
            #
            # Why?
            #
            # New data must be transformed exactly
            # like the training data.
            preprocessor = load_object(
                file_path=preprocessor_path
            )

            print("After Loading")

            # Transform user input.
            #
            # Why?
            #
            # Convert text into numbers,
            # scale numerical values,
            # and apply all preprocessing.
            data_scaled = preprocessor.transform(
                features
            )

            # Predict output.
            #
            # Why?
            #
            # The trained model predicts
            # the target value.
            preds = model.predict(
                data_scaled
            )

            # Return prediction.
            return preds

        except Exception as e:

            # Raise custom exception
            # if any error occurs.
            raise CustomException(e, sys)


# ==========================================================
# CustomData Class
#
# Why?
#
# Collect all user input
# in one object.
#
# Later convert it into
# a Pandas DataFrame.
#
# ==========================================================
class CustomData:

    # Constructor
    #
    # Receives all user inputs.
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int
    ):

        # Store Gender
        self.gender = gender

        # Store Race
        self.race_ethnicity = race_ethnicity

        # Store Parent Education
        self.parental_level_of_education = parental_level_of_education

        # Store Lunch Type
        self.lunch = lunch

        # Store Test Preparation
        self.test_preparation_course = test_preparation_course

        # Store Reading Score
        self.reading_score = reading_score

        # Store Writing Score
        self.writing_score = writing_score

    # ======================================================
    # Convert User Input to DataFrame
    #
    # Why?
    #
    # The preprocessing pipeline
    # expects a Pandas DataFrame.
    #
    # ======================================================
    def get_data_as_data_frame(self):

        try:

            # Create dictionary.
            #
            # Why?
            #
            # DataFrame is created from this dictionary.
            custom_data_input_dict = {

                "gender": [self.gender],

                "race_ethnicity": [
                    self.race_ethnicity
                ],

                "parental_level_of_education": [
                    self.parental_level_of_education
                ],

                "lunch": [
                    self.lunch
                ],

                "test_preparation_course": [
                    self.test_preparation_course
                ],

                "reading_score": [
                    self.reading_score
                ],

                "writing_score": [
                    self.writing_score
                ],
            }

            # Convert dictionary into DataFrame.
            #
            # Why?
            #
            # Preprocessor.transform()
            # requires DataFrame input.
            return pd.DataFrame(
                custom_data_input_dict
            )

        except Exception as e:

            raise CustomException(e, sys)