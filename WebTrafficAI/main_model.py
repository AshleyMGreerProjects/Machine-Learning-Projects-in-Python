import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tensorflow as tf
from feature_engineering import feature_engineering
from hyperparameter_tuning import hyperparameter_tuning
from model_evaluation import evaluate_models
from data_visualization import visualize_data, visualize_predictions
from google.oauth2 import service_account
from googleapiclient.discovery import build
from error_handling import handle_google_analytics_error, handle_data_processing_error, handle_model_training_error, handle_visualization_error, handle_hyperparameter_tuning_error, handle_general_error

# Set up Google Analytics API
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'path_to_your_service_account.json'  # Replace with the path to your JSON key file
VIEW_ID = 'your_view_id'  # Replace with your Google Analytics View ID

try:
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
except Exception as e:
    error_message = handle_google_analytics_error(e)
    print(error_message)
    sys.exit(1)

# Function to get real-time data from Google Analytics
def get_realtime_data():
    try:
        response = analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': 'today', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:activeUsers'}],
                        'dimensions': [{'name': 'ga:source'}]
                    }]
            }
        ).execute()
    
        rows = response.get('reports', [])[0].get('data', {}).get('rows', [])
        data = pd.DataFrame([{'Source': row['dimensions'][0], 'Active Users': row['metrics'][0]['values'][0]} for row in rows])
        return data
    except Exception as e:
        error_message = handle_google_analytics_error(e)
        print(error_message)
        return None

# Step 1: Load data from free sources or Google Analytics
def load_data(source='kaggle'):
    try:
        if source == 'kaggle':
            # Example dataset from Kaggle
            url = 'https://www.kaggle.com/'
            df = pd.read_csv(url)
        elif source == 'datagov':
            # Example dataset from Data.gov
            url = 'https://data.gov/'
            df = pd.read_csv(url)
        elif source == 'google_analytics':
            df = get_realtime_data()  # Get live data from Google Analytics
        else:
            raise ValueError("Invalid source. Choose 'kaggle', 'datagov', or 'google_analytics'.")
        return df
    except Exception as e:
        error_message = handle_data_processing_error(e)
        print(error_message)
        return None

# Step 2: Data Preprocessing
def preprocess_data(df):
    try:
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        df = feature_engineering(df)
        for col in ['Page Views', 'Clicks', 'Session Duration', 'Bounce Rate', 'User Traffic', 'PageViews_per_Click', 'SessionDuration_per_PageView']:
            if col in df.columns:
                df[col] = df[col].astype(float)
        df = df.fillna(method='ffill')
        return df
    except Exception as e:
        error_message = handle_data_processing_error(e)
        print(error_message)
        return None

# Step 3: Train Models
def train_model(model_name, df):
    try:
        X = df[['Page Views', 'Clicks', 'Session Duration', 'Bounce Rate', 'IsWeekend', 'PageViews_per_Click', 'SessionDuration_per_PageView']]
        y = df['User Traffic']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        if model_name == 'Linear Regression':
            model = LinearRegression()
        elif model_name == 'Random Forest':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_name == 'TensorFlow Neural Network':
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
            y_pred = model.predict(X_test).flatten()
            return mean_squared_error(y_test, y_pred)
        
        # For Linear Regression and Random Forest
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        
        return mse
    except Exception as e:
        error_message = handle_model_training_error(e)
        print(error_message)
        return None

# Step 4: Create GUI
def create_gui():
    root = ttk.Window(title="User Traffic Predictor", themename="darkly")
    
    # Data Source Dropdown
    source_label = ttk.Label(root, text="Select Data Source:")
    source_label.pack(padx=10, pady=5)
    
    source_var = ttk.StringVar(value='kaggle')
    source_dropdown = ttk.Combobox(root, textvariable=source_var, values=['kaggle', 'datagov', 'google_analytics'])
    source_dropdown.pack(padx=10, pady=5)
    
    # Model Selection Dropdown
    model_label = ttk.Label(root, text="Select Model:")
    model_label.pack(padx=10, pady=5)
    
    model_var = ttk.StringVar(value='Linear Regression')
    model_dropdown = ttk.Combobox(root, textvariable=model_var, values=['Linear Regression', 'Random Forest', 'TensorFlow Neural Network'])
    model_dropdown.pack(padx=10, pady=5)
    
    # Train Button
    def on_train():
        source = source_var.get()
        model_name = model_var.get()
        df = load_data(source)
        if df is not None:
            df = preprocess_data(df)
            if df is not None:
                mse = train_model(model_name, df)
                if mse is not None:
                    result_label.config(text=f"{model_name} MSE: {mse:.2f}")
    
    # Hyperparameter Tuning Button
    def on_tune():
        source = source_var.get()
        model_name = model_var.get()
        df = load_data(source)
        if df is not None:
            df = preprocess_data(df)
            if df is not None:
                try:
                    best_params, mse = hyperparameter_tuning(df, model_name)
                except Exception as e:
                    error_message = handle_hyperparameter_tuning_error(e)
                    print(error_message)
                    return None
                if mse is not None:
                    result_label.config(text=f"Best Params: {best_params}\n{model_name} Tuned MSE: {mse:.2f}")
    
    tune_button = ttk.Button(root, text="Tune Hyperparameters", command=on_tune, bootstyle=INFO)
    tune_button.pack(padx=10, pady=5)
    
    # Model Evaluation Button
    def on_evaluate():
        source = source_var.get()
        df = load_data(source)
        if df is not None:
            df = preprocess_data(df)
            if df is not None:
                results = evaluate_models(df)
                
                result_text = "Model Evaluation:\n"
                for model, metrics in results.items():
                    result_text += f"{model} - MSE: {metrics['MSE']:.2f}, MAE: {metrics['MAE']:.2f}, R2: {metrics['R2 Score']:.2f}\n"
                
                result_label.config(text=result_text)
    
    evaluate_button = ttk.Button(root, text="Evaluate Models", command=on_evaluate, bootstyle=WARNING)
    evaluate_button.pack(padx=10, pady=5)
    
    # Data Visualization Button
    def on_visualize():
        source = source_var.get()
        df = load_data(source)
        if df is not None:
            df = preprocess_data(df)
            if df is not None:
                try:
                    visualize_data(df)
                except Exception as e:
                    error_message = handle_visualization_error(e)
                    print(error_message)
    
    visualize_button = ttk.Button(root, text="Visualize Data", command=on_visualize, bootstyle=PRIMARY)
    visualize_button.pack(padx=10, pady=5)
    
    # Display Results
    result_label = ttk.Label(root, text="")
    result_label.pack(padx=10, pady=10)
    
    root.mainloop()

# Run the GUI application
create_gui()