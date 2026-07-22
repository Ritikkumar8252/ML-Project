# ==========================================================
# Import Required Libraries
# ==========================================================

# Flask is used to create the web application.
from flask import Flask, request, render_template

# NumPy is used for numerical operations.
# (Not used in this file, can be removed if unnecessary.)
import numpy as np

# Pandas is used to work with DataFrames.
# The prediction pipeline converts user input into a DataFrame.
import pandas as pd

# StandardScaler is imported but not used here.
# Scaling is already handled inside preprocessor.pkl.
# This import can be removed.
from sklearn.preprocessing import StandardScaler

# Import CustomData and PredictPipeline classes.
#
# CustomData:
# Collects user input and converts it into a DataFrame.
#
# PredictPipeline:
# Loads the saved model and preprocessor,
# transforms the input, and predicts the result.
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


# ==========================================================
# Create Flask Application
# ==========================================================

# __name__ tells Flask where the application is located.
# Flask uses this to find templates, static files, etc.
application = Flask(__name__)

# Create another variable pointing to the same Flask app.
#
# Why?
#
# Deployment platforms like Gunicorn often look for a variable
# named "application", while locally we usually run "app".
#
# Both refer to the same Flask application.
app = application


# ==========================================================
# Home Page Route
# ==========================================================

# Route '/'
#
# Why?
#
# When the user opens:
#
# http://localhost:5000/
#
# this function runs automatically.
@app.route('/')
def index():

    # Render the homepage.
    # Flask looks inside the templates folder.
    return render_template('index.html')


# ==========================================================
# Prediction Route
# ==========================================================

# This route handles both:
#
# GET  -> Open prediction form.
#
# POST -> Receive form data and make prediction.
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():

    # ------------------------------------------------------
    # GET Request
    # ------------------------------------------------------
    #
    # Why?
    #
    # When the user first opens the prediction page,
    # no data has been submitted yet.
    #
    # Simply display the input form.
    if request.method == 'GET':

        return render_template('home.html')

    # ------------------------------------------------------
    # POST Request
    # ------------------------------------------------------
    #
    # Why?
    #
    # The user clicked the Predict button.
    #
    # Flask receives all form values here.
    else:

        # Create CustomData object.
        #
        # Why?
        #
        # Instead of passing many variables separately,
        # we store all user inputs inside one object.
        data = CustomData(

            # Get Gender from HTML form.
            gender=request.form.get('gender'),

            # Get Race/Ethnicity.
            race_ethnicity=request.form.get('ethnicity'),

            # Get Parent Education.
            parental_level_of_education=request.form.get(
                'parental_level_of_education'
            ),

            # Get Lunch Type.
            lunch=request.form.get('lunch'),

            # Get Test Preparation Status.
            test_preparation_course=request.form.get(
                'test_preparation_course'
            ),

            # Reading Score
            #
            # request.form returns text.
            #
            # float() converts it into a number.
            reading_score=float(request.form.get('writing_score')),

            # Writing Score
            writing_score=float(request.form.get('reading_score'))

        )

        # --------------------------------------------------
        # Convert User Input into DataFrame
        # --------------------------------------------------
        #
        # Why?
        #
        # Machine Learning preprocessing expects
        # a Pandas DataFrame.
        pred_df = data.get_data_as_data_frame()

        # Print DataFrame in terminal.
        # Useful for debugging.
        print(pred_df)

        print("Before Prediction")

        # --------------------------------------------------
        # Create Prediction Pipeline
        # --------------------------------------------------
        #
        # Why?
        #
        # PredictPipeline performs:
        #
        # 1. Load preprocessor.pkl
        # 2. Transform input
        # 3. Load model.pkl
        # 4. Predict output
        predict_pipeline = PredictPipeline()

        print("Mid Prediction")

        # --------------------------------------------------
        # Predict
        # --------------------------------------------------
        #
        # Pass DataFrame to prediction pipeline.
        results = predict_pipeline.predict(pred_df)

        print("After Prediction")

        # --------------------------------------------------
        # Display Prediction
        # --------------------------------------------------
        #
        # results is usually an array like:
        #
        # [78.56]
        #
        # results[0] extracts the actual prediction.
        return render_template(

            'home.html',

            results=results[0]

        )


# ==========================================================
# Main Function
# ==========================================================

# Why?
#
# __name__ == "__main__"
#
# means this file is being run directly.
#
# If imported into another file,
# app.run() will not execute.
if __name__ == "__main__":

    # Start Flask Development Server.
    #
    # host="0.0.0.0"
    #
    # Why?
    #
    # Makes the application accessible
    # from other devices on the same network.
    #
    # Default Port = 5000
    # app.run(host="0.0.0.0")   
    # this not show url in terminal  direct search in the browser
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )