# ==========================
# Import Required Libraries
# ==========================

import os  # Used for working with folders and file paths
import sys  # Used to get system information (mainly for custom exception handling)

# Import custom exception class
from src.exception import CustomException

# Import logging configuration
from src.logger import logging

# Pandas is used to read and work with CSV files
import pandas as pd

# Used to split the dataset into training and testing data
from sklearn.model_selection import train_test_split

# Used to create a configuration class easily
from dataclasses import dataclass

# Import Data Transformation component
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# # Import Model Trainer component
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer


# ==========================================================
# Configuration Class
# Stores all file paths used in Data Ingestion
# ==========================================================

@dataclass  #saves you from writing repetitive code.
class DataIngestionConfig:

    # Path where training data will be saved
    train_data_path: str = os.path.join("artifacts", "train.csv")

    # Path where testing data will be saved
    test_data_path: str = os.path.join("artifacts", "test.csv")

    # Path where the original (raw) dataset will be saved
    raw_data_path: str = os.path.join("artifacts", "data.csv")


# ==========================================================
# Data Ingestion Class
# Responsible for:
# 1. Reading the dataset
# 2. Saving raw data
# 3. Splitting into train and test data
# 4. Saving train and test CSV files
# ==========================================================

class DataIngestion:

    # Constructor
    # Runs automatically when an object is created
    def __init__(self):

        # Create an object of the configuration class
        # Now we can access all file paths using self.ingestion_config
        self.ingestion_config = DataIngestionConfig()

    # Main function for Data Ingestion
    def initiate_data_ingestion(self):

        # Log message
        logging.info("Entered the data ingestion component")

        try:

            # =====================================
            # Step 1: Read CSV File
            # =====================================

            # Read dataset into a Pandas DataFrame
            df = pd.read_csv("notebook/data/stud (1).csv")

            logging.info("Dataset loaded successfully")

            # =====================================
            # Step 2: Create Artifacts Folder
            # =====================================

            # os.path.dirname("artifacts/train.csv")
            # returns "artifacts"

            # If the folder doesn't exist, create it.
            # exist_ok=True prevents an error if it already exists.
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True
            )

            # =====================================
            # Step 3: Save Raw Dataset
            # =====================================

            # Save the original dataset without any changes
            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,
                header=True
            )

            logging.info("Raw dataset saved")

            # =====================================
            # Step 4: Split Dataset
            # =====================================

            logging.info("Train-test split started")

            # Split data:
            # 80% → Training
            # 20% → Testing

            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )

            # random_state=42 ensures the split is the same
            # every time you run the code.

            # =====================================
            # Step 5: Save Training Data
            # =====================================

            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            # =====================================
            # Step 6: Save Testing Data
            # =====================================

            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            logging.info("Data Ingestion completed successfully")

            # =====================================
            # Step 7: Return File Paths
            # =====================================

            # These paths will be used by the next component
            # (Data Transformation)
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        # =====================================
        # Exception Handling
        # =====================================

        except Exception as e:

            # If any error occurs,
            # send it to the custom exception class.
            raise CustomException(e, sys)


# ==========================================================
# Main Function
# This code runs only when this file is executed directly.
# ==========================================================

if __name__ == "__main__":

    # Create object of DataIngestion class
    obj = DataIngestion()

    # Run Data Ingestion
    # Returns:
    # artifacts/train.csv
    # artifacts/test.csv
    train_data, test_data = obj.initiate_data_ingestion()

    # =====================================
    # Data Transformation
    # =====================================

    # Create object of DataTransformation class
    data_transformation = DataTransformation()

    # Perform preprocessing:
    # - Handle missing values
    # - Encode categorical columns
    # - Scale numerical columns
    # Returns transformed NumPy arrays
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data,
        test_data
    )

    # =====================================
    # Model Training
    # =====================================

    # Create object of ModelTrainer
    modeltrainer = ModelTrainer()

    # Train different ML models
    # Compare their performance
    # Save the best model
    # Print the model score (usually R² Score)
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))