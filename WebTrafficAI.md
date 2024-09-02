# WebTrafficAI

WebTrafficAI is a machine learning project designed to forecast website traffic using various features extracted from user interactions. This repository contains multiple Python scripts that cover the entire machine learning pipeline, from data preprocessing and feature engineering to model training, evaluation, and visualization.

## Project Structure

### 1. `data_visualization.py`

This script is responsible for visualizing the data and the model predictions. It includes functions to generate pair plots of the dataset and to plot actual versus predicted values.

- **Functions:**
  - `visualize_data(df)`: Takes a DataFrame `df` as input and generates a pair plot using Seaborn, which helps in visualizing relationships between variables.
  - `visualize_predictions(y_test, y_pred, model_name)`: Plots the actual versus predicted values for a given model, allowing for a visual comparison of the model's performance.

### 2. `error_handling.py`

This script provides error handling functionalities, particularly for logging exceptions and handling specific errors related to data processing and Google Analytics API interactions.

- **Functions:**
  - `log_exception(exc_type, exc_value, exc_traceback)`: Logs uncaught exceptions, which are useful for debugging.
  - `handle_google_analytics_error(e)`: Handles errors specifically related to the Google Analytics API, providing user-friendly error messages and logging.
  - `handle_data_processing_error(e)`: Catches and logs errors during data processing, such as file parsing or data manipulation errors.
  - `handle_visualization_error(e)`: Manages errors that occur during the visualization process, ensuring the application does not crash unexpectedly.

### 3. `feature_engineering.py`

This script focuses on creating and engineering features that will be used in the machine learning models. It also includes preprocessing steps necessary for model training.

- **Functions:**
  - `preprocess_data(df)`: Handles data cleaning and preprocessing, including handling missing values, scaling numerical features, and encoding categorical variables.
  - `feature_engineering(df)`: Creates additional features such as `PageViews_per_Click` and `SessionDuration_per_PageView` from the raw data, which are intended to enhance the predictive power of the models.

### 4. `hyperparameter_tuning.py`

This script is dedicated to tuning the hyperparameters of machine learning models to optimize their performance.

- **Functions:**
  - `tune_hyperparameters(model, param_grid, X_train, y_train)`: Performs a grid search over the specified hyperparameter grid `param_grid` to find the best parameters for the given model. This function returns the best model configuration based on cross-validation performance.

### 5. `main_model.py`

The main script where the entire model pipeline is orchestrated, including loading data, feature engineering, model training, hyperparameter tuning, and visualization.

- **Functions:**
  - `load_data(source)`: Loads data from the specified source, which can be a CSV file or a database.
  - `train_and_evaluate_models()`: Trains the machine learning models using the engineered features, evaluates their performance, and visualizes the results.
  - `create_gui()`: Creates a simple graphical user interface (GUI) using `tkinter` to allow users to interact with the model, visualize data, and evaluate different models easily.

### 6. `model_evaluation.py`

This script is responsible for evaluating the performance of different machine learning models using various metrics.

- **Functions:**
  - `evaluate_models(df)`: Trains and evaluates multiple models (e.g., Linear Regression, Random Forest) on the provided dataset. The function returns a dictionary containing the Mean Squared Error (MSE), Mean Absolute Error (MAE), and R-squared (R2) score for each model.

## Key Features

- **Modular Codebase**: Each component of the machine learning pipeline is modularized into separate scripts, making it easier to manage and update.
- **Comprehensive Error Handling**: The project includes robust error handling mechanisms to ensure smooth execution and easier debugging.
- **Feature Engineering**: The `feature_engineering.py` script adds new features to improve the model's predictive capabilities.
- **Hyperparameter Tuning**: The `hyperparameter_tuning.py` script optimizes model performance by selecting the best hyperparameters.
- **Visualization**: The `data_visualization.py` script provides tools for visualizing both the raw data and the model outputs.

## Future Work

- **Integration with Real-Time Data Sources**: Extend the model to work with real-time data streams.
- **Deployment**: Package the application for deployment as a web service, allowing users to input data and get traffic predictions on-demand.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
