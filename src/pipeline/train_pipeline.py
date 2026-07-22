# ==========================================================
# Train Pipeline
#
# Why do we need this file?
#
# This file connects all the ML components together.
#
# Instead of manually running:
#
# 1. Data Ingestion
# 2. Data Transformation
# 3. Model Training
#
# one by one, this TrainPipeline class runs them
# automatically in the correct order.
#
# Overall Flow
#
# Dataset
#     │
#     ▼
# Data Ingestion
#     │
#     ▼
# Data Transformation
#     │
#     ▼
# Model Training
#     │
#     ▼
# Save model.pkl
# Save preprocessor.pkl
#
# ==========================================================


# Used to access system information.
#
# Why?
#
# If an error occurs, sys helps CustomException
# identify the file name and line number.
import sys


# Used for file and directory operations.
#
# Although not used directly in this file,
# it is commonly imported for path handling.
import os


# Import CustomException.
#
# Why?
#
# Instead of showing Python's default error,
# this displays a cleaner error message with
# file name and line number.
from src.exception import CustomException


# Import Data Ingestion Component.
#
# Why?
#
# Responsible for:
#
# ✔ Reading dataset
# ✔ Splitting train/test data
# ✔ Saving train.csv and test.csv
from src.components.data_ingestion import DataIngestion


# Import Data Transformation Component.
#
# Why?
#
# Responsible for:
#
# ✔ Handling missing values
# ✔ Encoding categorical columns
# ✔ Scaling numerical columns
# ✔ Saving preprocessor.pkl
from src.components.data_transformation import DataTransformation


# Import Model Trainer Component.
#
# Why?
#
# Responsible for:
#
# ✔ Training multiple models
# ✔ Comparing performance
# ✔ Selecting best model
# ✔ Saving model.pkl
from src.components.model_trainer import ModelTrainer


# ==========================================================
# TrainPipeline Class
#
# Why?
#
# This class controls the complete
# Machine Learning training process.
#
# It acts like a manager.
#
# Instead of calling every component manually,
# this class runs everything in sequence.
#
# ==========================================================
class TrainPipeline:

    # Constructor
    #
    # Why?
    #
    # Called automatically whenever
    # TrainPipeline object is created.
    #
    # Example:
    #
    # pipeline = TrainPipeline()
    #
    # Since no initialization is required,
    # we simply use pass.
    def __init__(self):
        pass

    # ======================================================
    # Train Function
    #
    # Why?
    #
    # This function runs the complete
    # Machine Learning pipeline.
    #
    # Steps:
    #
    # Read Dataset
    # ↓
    # Split Dataset
    # ↓
    # Transform Data
    # ↓
    # Train Models
    # ↓
    # Save model.pkl
    # ↓
    # Return R² Score
    #
    # ======================================================
    def train(self):

        try:

            # ---------------------------------------------
            # Step 1 : Data Ingestion
            # ---------------------------------------------
            #
            # Create DataIngestion object.
            data_ingestion = DataIngestion()

            # Read dataset.
            #
            # Split dataset into:
            #
            # train.csv
            # test.csv
            #
            # Returns paths of both files.
            train_data, test_data = (
                data_ingestion.initiate_data_ingestion()
            )

            # ---------------------------------------------
            # Step 2 : Data Transformation
            # ---------------------------------------------
            #
            # Create DataTransformation object.
            data_transformation = DataTransformation()

            # Transform both datasets.
            #
            # Operations performed:
            #
            # ✔ Missing Value Handling
            # ✔ Encoding
            # ✔ Scaling
            #
            # Returns:
            #
            # train_arr
            # test_arr
            # preprocessor.pkl path
            train_arr, test_arr, _ = (
                data_transformation.initiate_data_transformation(
                    train_data,
                    test_data
                )
            )

            # ---------------------------------------------
            # Step 3 : Model Training
            # ---------------------------------------------
            #
            # Create ModelTrainer object.
            model_trainer = ModelTrainer()

            # Train multiple ML models.
            #
            # Compare their performance.
            #
            # Select best model.
            #
            # Save best model as:
            #
            # artifacts/model.pkl
            #
            # Returns R² Score.
            r2_square = (
                model_trainer.initiate_model_trainer(
                    train_arr,
                    test_arr
                )
            )

            # Return model accuracy.
            return r2_square

        except Exception as e:

            # If any error occurs in any step,
            # raise a CustomException with
            # detailed information.
            raise CustomException(e, sys)


# ==========================================================
# Main Function
#
# Why?
#
# This block runs only when this file
# is executed directly.
#
# Example:
#
# python train_pipeline.py
#
# It will NOT execute if this file
# is imported into another Python file.
#
# ==========================================================
if __name__ == "__main__":

    # Create TrainPipeline object.
    pipeline = TrainPipeline()

    # Start complete ML training process.
    #
    # Flow:
    #
    # Data Ingestion
    # ↓
    # Data Transformation
    # ↓
    # Model Training
    # ↓
    # Save model.pkl
    # ↓
    # Save preprocessor.pkl
    pipeline.train()