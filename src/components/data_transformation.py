# ==========================================================
# Import Required Libraries
# ==========================================================

import sys                     # Used for exception handling
import os                      # Used for file and folder operations

# Used to create simple configuration classes
from dataclasses import dataclass

# NumPy is used for numerical operations
import numpy as np

# Pandas is used to read CSV files
import pandas as pd

# ColumnTransformer allows different preprocessing
# for different types of columns
from sklearn.compose import ColumnTransformer

# Used to fill missing values
from sklearn.impute import SimpleImputer

# Pipeline connects multiple preprocessing steps together
from sklearn.pipeline import Pipeline

# OneHotEncoder converts categorical values into numbers
# StandardScaler scales numerical values
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Import custom exception class
from src.exception import CustomException

# Import logger
from src.logger import logging

# Function used to save Python objects (pickle)
from src.utils import save_object


# ==========================================================
# Configuration Class
# Stores the path where the preprocessor will be saved
# ==========================================================

@dataclass
class DataTransformationConfig:

    # File where the preprocessing pipeline will be stored
    preprocessor_obj_file_path = os.path.join(
        "artifacts",
        "preprocessor.pkl"
    )


# ==========================================================
# Data Transformation Class
# Responsible for converting raw data into
# machine-learning-ready data
# ==========================================================

class DataTransformation:

    # Constructor
    def __init__(self):

        # Create configuration object
        self.data_transformation_config = DataTransformationConfig()

    # ======================================================
    # Create Preprocessing Pipeline
    # ======================================================

    def get_data_transformer_object(self):

        """
        Creates and returns the preprocessing pipeline.
        """

        try:

            # Numerical columns
            numerical_columns = [
                "writing_score",
                "reading_score"
            ]

            # Categorical columns
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            # ==================================================
            # Numerical Pipeline
            # ==================================================

            # Step 1:
            # Replace missing values with median

            # Step 2:
            # Scale numerical values

            num_pipeline = Pipeline(

                steps=[

                    (
                        "imputer",
                        SimpleImputer(strategy="median")
                    ),

                    (
                        "scaler",
                        StandardScaler()
                    )

                ]

            )

            # ==================================================
            # Categorical Pipeline
            # ==================================================

            # Step 1:
            # Replace missing values using most frequent value

            # Step 2:
            # Convert text into numbers

            # Step 3:
            # Scale encoded values

            cat_pipeline = Pipeline(

                steps=[

                    (
                        "imputer",
                        SimpleImputer(strategy="most_frequent")
                    ),

                    (
                        "one_hot_encoder",
                        OneHotEncoder()
                    ),

                    (
                        "scaler",
                        StandardScaler(with_mean=False)
                    )

                ]

            )

            logging.info(
                f"Categorical Columns : {categorical_columns}"
            )

            logging.info(
                f"Numerical Columns : {numerical_columns}"
            )

            # ==================================================
            # Combine Both Pipelines
            # ==================================================

            # Numerical columns go through num_pipeline

            # Categorical columns go through cat_pipeline

            preprocessor = ColumnTransformer(

                [

                    (
                        "num_pipeline",
                        num_pipeline,
                        numerical_columns
                    ),

                    (
                        "cat_pipeline",
                        cat_pipeline,
                        categorical_columns
                    )

                ]

            )

            # Return preprocessing object
            return preprocessor

        except Exception as e:

            raise CustomException(e, sys)

    # ======================================================
    # Main Transformation Function
    # ======================================================

    def initiate_data_transformation(
        self,
        train_path,
        test_path
    ):

        try:

            # Read train dataset
            train_df = pd.read_csv(train_path)

            # Read test dataset
            test_df = pd.read_csv(test_path)

            logging.info(
                "Train and Test datasets loaded."
            )

            logging.info(
                "Creating preprocessing object."
            )

            # Get preprocessing pipeline
            preprocessing_obj = self.get_data_transformer_object()

            # Target column
            target_column_name = "math_score"

            # ==================================================
            # Separate Input and Target
            # ==================================================

            # Training Input Features (X_train)

            input_feature_train_df = train_df.drop(
                columns=[target_column_name]
            )

            # Training Target (y_train)

            target_feature_train_df = train_df[target_column_name]

            # Testing Input Features (X_test)

            input_feature_test_df = test_df.drop(
                columns=[target_column_name]
            )

            # Testing Target (y_test)

            target_feature_test_df = test_df[target_column_name]

            logging.info(
                "Applying preprocessing pipeline."
            )

            # ==================================================
            # Fit and Transform Training Data
            # ==================================================

            # Learn preprocessing from training data

            input_feature_train_arr = (
                preprocessing_obj.fit_transform(
                    input_feature_train_df
                )
            )

            # ==================================================
            # Transform Test Data
            # ==================================================

            # Apply same preprocessing on test data

            input_feature_test_arr = (
                preprocessing_obj.transform(
                    input_feature_test_df
                )
            )

            # ==================================================
            # Combine Features and Target
            # ==================================================

            train_arr = np.c_[

                input_feature_train_arr,

                np.array(target_feature_train_df)

            ]

            test_arr = np.c_[

                input_feature_test_arr,

                np.array(target_feature_test_df)

            ]

            logging.info(
                "Saving preprocessing object."
            )

            # ==================================================
            # Save Preprocessor
            # ==================================================

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,

                obj=preprocessing_obj

            )

            # ==================================================
            # Return Data
            # ==================================================

            return (

                train_arr,

                test_arr,

                self.data_transformation_config.preprocessor_obj_file_path

            )

        except Exception as e:

            raise CustomException(e, sys)