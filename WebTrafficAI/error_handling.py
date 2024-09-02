import logging
import sys
import traceback
from google.auth.exceptions import GoogleAuthError
from googleapiclient.errors import HttpError
import pandas as pd
from sklearn.exceptions import NotFittedError
from matplotlib import pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(filename='app_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_exception(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Install exception hook
sys.excepthook = log_exception

def handle_google_analytics_error(e):
    """Handle Google Analytics API errors."""
    if isinstance(e, GoogleAuthError):
        logging.error("Authentication error with Google Analytics: %s", e)
        return "Authentication error. Please check your credentials."
    elif isinstance(e, HttpError):
        logging.error("HTTP error with Google Analytics API: %s", e)
        return "Google Analytics API request failed. Please check your API key and internet connection."
    else:
        logging.error("Unknown error with Google Analytics: %s", e)
        return "An unknown error occurred while accessing Google Analytics."

def handle_data_processing_error(e):
    """Handle data processing errors."""
    if isinstance(e, pd.errors.ParserError):
        logging.error("Data parsing error: %s", e)
        return "Error parsing data. Please check the format of your input data."
    elif isinstance(e, KeyError):
        logging.error("Key error during data processing: %s", e)
        return "Missing key in data processing. Please ensure the data contains the expected columns."
    else:
        logging.error("Unknown error during data processing: %s", e)
        return "An unknown error occurred during data processing."

def handle_model_training_error(e):
    """Handle model training errors."""
    if isinstance(e, NotFittedError):
        logging.error("Model fitting error: %s", e)
        return "Model not fitted. Please ensure the model is trained before making predictions."
    else:
        logging.error("Unknown error during model training: %s", e)
        return "An unknown error occurred during model training."

def handle_visualization_error(e):
    """Handle data visualization errors."""
    if isinstance(e, ValueError):
        logging.error("Value error during data visualization: %s", e)
        return "Error during data visualization. Please check the input data."
    elif isinstance(e, plt.error):
        logging.error("Matplotlib error during visualization: %s", e)
        return "Visualization error with Matplotlib. Please check your plots."
    elif isinstance(e, sns.errors.SeabornError):
        logging.error("Seaborn error during visualization: %s", e)
        return "Visualization error with Seaborn. Please check your plots."
    else:
        logging.error("Unknown error during data visualization: %s", e)
        return "An unknown error occurred during data visualization."

def handle_hyperparameter_tuning_error(e):
    """Handle errors during hyperparameter tuning."""
    logging.error("Error during hyperparameter tuning: %s", e)
    return "An error occurred during hyperparameter tuning. Please check your parameters and try again."

def handle_general_error(e):
    """Handle any other general errors."""
    logging.error("General error: %s", e)
    return "An unexpected error occurred. Please check the logs for more details."