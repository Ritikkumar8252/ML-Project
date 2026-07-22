# ==========================================================
# MODEL TRAINER
# This file is responsible for:
# 1. Receiving transformed training and testing data.
# 2. Training multiple machine learning models.
# 3. Finding the best hyperparameters using GridSearchCV.
# 4. Comparing all models using R² Score.
# 5. Selecting the best-performing model.
# 6. Saving the best model as model.pkl.
# ==========================================================

# Used to work with files and folder paths.
# We use it to create the path where the trained model will be saved.
import os

# Used to get system information.
# It helps CustomException display the filename and line number if an error occurs.
import sys

# @dataclass automatically creates constructor (__init__) and stores configuration values.
# We use it because this class only stores settings, not logic.
from dataclasses import dataclass

# ================= Machine Learning Models =================

# Random Forest combines many Decision Trees to improve accuracy.
from sklearn.ensemble import RandomForestRegressor

# Decision Tree predicts by splitting the dataset into branches.
from sklearn.tree import DecisionTreeRegressor

# Gradient Boosting builds trees one after another to reduce previous errors.
from sklearn.ensemble import GradientBoostingRegressor

# AdaBoost combines many weak learners into one strong learner.
from sklearn.ensemble import AdaBoostRegressor

# Linear Regression fits the best straight line through the data.
from sklearn.linear_model import LinearRegression

# XGBoost is an advanced boosting algorithm known for high performance.
from xgboost import XGBRegressor

# CatBoost works especially well with categorical data.
from catboost import CatBoostRegressor

# KNN is imported but not used in this project.
# It can be removed if not required.
from sklearn.neighbors import KNeighborsRegressor

# Used to measure regression model performance.
# Higher R² score means better predictions.
from sklearn.metrics import r2_score

# ================= Project Files =================

# Custom exception gives detailed error messages.
from src.exception import CustomException

# Logging records program execution.
from src.logger import logging

# save_object() saves the trained model.
# evaluate_models() trains multiple models and compares them.
from src.utils import save_object, evaluate_models


# ==========================================================
# Configuration Class
# Why?
# Instead of writing "artifacts/model.pkl" everywhere,
# we store it once here.
# If the save location changes, only this file needs updating.
# ==========================================================
@dataclass
class ModelTrainerConfig:

    # Path where the trained model will be saved.
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


# ==========================================================
# ModelTrainer Class
#
# Why create a class?
#
# It keeps everything related to model training together.
#
# ModelTrainer
# ├── Train Models
# ├── Compare Models
# ├── Save Best Model
# └── Return Final Accuracy
# ==========================================================
class ModelTrainer:

    # Constructor
    # Runs automatically whenever ModelTrainer() is created.
    def __init__(self):

        # Create configuration object.
        # Now we can access
        # self.model_trainer_config.trained_model_file_path
        self.model_trainer_config = ModelTrainerConfig()

    # ======================================================
    # Main Training Function
    #
    # Why?
    # This function performs the complete model training process.
    # ======================================================
    def initiate_model_trainer(self, train_array, test_array):

        try:

            # Save message in log file.
            logging.info("Split training and test input data")

            # ==================================================
            # Split Features (X) and Target (y)
            #
            # Dataset Example
            #
            # Math Reading Writing
            # 80     75      70
            # 90     88      92
            #
            # Last column is Target (Writing Score)
            #
            # X = Math + Reading
            # y = Writing
            # ==================================================

            X_train, y_train, X_test, y_test = (

                # Select every column except last
                train_array[:, :-1],

                # Select only last column
                train_array[:, -1],

                # Test Features
                test_array[:, :-1],

                # Test Target
                test_array[:, -1]

            )

            # ==================================================
            # Dictionary of Models
            #
            # Why Dictionary?
            #
            # Instead of writing
            #
            # Train RF
            # Train DT
            # Train XGB
            #
            # We simply loop through the dictionary.
            # ==================================================

            models = {

                "Random Forest": RandomForestRegressor(),

                "Decision Tree": DecisionTreeRegressor(),

                "Gradient Boosting": GradientBoostingRegressor(),

                "Linear Regression": LinearRegression(),

                "XGBRegressor": XGBRegressor(),

                "CatBoosting Regressor": CatBoostRegressor(verbose=False),

                "AdaBoost Regressor": AdaBoostRegressor(),

            }

            # ==================================================
            # Hyperparameters
            #
            # Why?
            #
            # Every ML model has settings called Hyperparameters.
            #
            # Example:
            #
            # Random Forest
            #
            # 100 Trees
            # 200 Trees
            # 300 Trees
            #
            # GridSearchCV will automatically test all combinations
            # and choose the best one.
            # ==================================================

            params = {

                "Decision Tree": {

                    # Different methods to calculate the best split.
                    "criterion": [
                        "squared_error",
                        "friedman_mse",
                        "absolute_error",
                        "poisson",
                    ]
                },

                "Random Forest": {

                    # Number of trees to build.
                    "n_estimators": [
                        8,
                        16,
                        32,
                        64,
                        128,
                        256,
                    ]
                },

                "Gradient Boosting": {

                    # Learning speed.
                    "learning_rate": [
                        0.1,
                        0.01,
                        0.05,
                        0.001,
                    ],

                    # Percentage of training data used.
                    "subsample": [
                        0.6,
                        0.7,
                        0.75,
                        0.8,
                        0.85,
                        0.9,
                    ],

                    # Number of boosting rounds.
                    "n_estimators": [
                        8,
                        16,
                        32,
                        64,
                        128,
                        256,
                    ]
                },

                # Linear Regression has no hyperparameters.
                "Linear Regression": {},

                "XGBRegressor": {

                    "learning_rate": [
                        0.1,
                        0.01,
                        0.05,
                        0.001,
                    ],

                    "n_estimators": [
                        8,
                        16,
                        32,
                        64,
                        128,
                        256,
                    ]
                },

                "CatBoosting Regressor": {

                    "depth": [6, 8, 10],

                    "learning_rate": [
                        0.01,
                        0.05,
                        0.1,
                    ],

                    "iterations": [
                        30,
                        50,
                        100,
                    ]
                },

                "AdaBoost Regressor": {

                    "learning_rate": [
                        0.1,
                        0.01,
                        0.5,
                        0.001,
                    ],

                    "n_estimators": [
                        8,
                        16,
                        32,
                        64,
                        128,
                        256,
                    ]
                }

            }

            # ==================================================
            # Train Every Model
            #
            # evaluate_models()
            #
            # Why?
            #
            # It trains every model,
            # performs GridSearchCV,
            # calculates R² Score,
            # and returns a dictionary.
            #
            # Example
            #
            # {
            # "Random Forest":0.91,
            # "Decision Tree":0.82
            # }
            # ==================================================

            model_report = evaluate_models(

                X_train=X_train,

                y_train=y_train,

                X_test=X_test,

                y_test=y_test,

                models=models,

                param=params

            )

            # ==================================================
            # Get Highest R² Score
            #
            # Why?
            #
            # Highest score means best-performing model.
            # ==================================================

            best_model_score = max(sorted(model_report.values()))

            # ==================================================
            # Find Model Name
            #
            # Why?
            #
            # We know the highest score,
            # now find which model achieved it.
            # ==================================================

            best_model_name = list(model_report.keys())[

                list(model_report.values()).index(best_model_score)

            ]

            # Retrieve the actual model object.

            best_model = models[best_model_name]

            # ==================================================
            # Check Model Performance
            #
            # If score is too low,
            # stop training.
            # ==================================================

            if best_model_score < 0.6:

                raise CustomException("No best model found", sys)

            logging.info("Best model selected successfully.")

            # ==================================================
            # Save Model
            #
            # Why?
            #
            # Training is expensive.
            # Save once and reuse many times.
            # ==================================================

            save_object(

                file_path=self.model_trainer_config.trained_model_file_path,

                obj=best_model

            )

            # ==================================================
            # Predict Test Data
            #
            # Why?
            #
            # We want to see how the best model performs
            # on unseen data.
            # ==================================================

            predicted = best_model.predict(X_test)

            # ==================================================
            # Calculate Final R² Score
            #
            # Why?
            #
            # It tells how accurate the best model is.
            # ==================================================

            r2_square = r2_score(y_test, predicted)

            # Return Final Performance Score

            return r2_square

        except Exception as e:

            # If any error occurs,
            # raise a detailed custom exception.

            raise CustomException(e, sys)