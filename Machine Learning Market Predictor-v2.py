import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
import pickle
import yfinance as yf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler

# Directories for caching data and saving models
CACHE_DIR = "cache"
MODEL_DIR = "models"
AVAILABLE_MODELS = {
    "Linear Regression": LinearRegression,
    "Random Forest": RandomForestRegressor,
    "LSTM": lambda input_shape: create_lstm_model(input_shape)
}

# Ensure cache and model directories exist
for directory in [CACHE_DIR, MODEL_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# LSTM Model Creation
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=100, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=100, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mean_squared_error')
    return model

# Step 1: Fetch Financial Data using yfinance
def scrape_data(stock_symbol):
    cache_file = os.path.join(CACHE_DIR, f"{stock_symbol}.csv")
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file, index_col='Date', parse_dates=True)
    else:
        df = yf.download(stock_symbol, period="5y")
        if df.empty:
            raise ValueError("No data found for this stock symbol.")
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        df.to_csv(cache_file)
    
    return df

# Step 1a: Feature Engineering
def add_technical_indicators(df):
    # Calculate moving averages
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # Calculate RSI and MACD
    df['RSI'] = compute_RSI(df)
    df['MACD'], df['Signal'] = compute_MACD(df)

    # Add lagged close prices
    for lag in range(1, 6):
        df[f'Close_lag_{lag}'] = df['Close'].shift(lag)

    # Drop any rows with NaN values (e.g., those caused by rolling calculations)
    df.dropna(inplace=True)

    # Debugging: Print the first few rows to check if features are added correctly
    print("Technical indicators and lag features added:")
    print(df.head())

    return df

def compute_RSI(df, window=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

def compute_MACD(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    MACD = exp1 - exp2
    Signal = MACD.ewm(span=9, adjust=False).mean()
    return MACD, Signal

# Step 2: Machine Learning Model for Stock Price Prediction
def train_model(df, model_name):
    model_file = os.path.join(MODEL_DIR, f"{df.name}_{model_name}.pkl")
    scaler = None
    if os.path.exists(model_file) and model_name != "LSTM":
        with open(model_file, 'rb') as f:
            model, mse = pickle.load(f)
    else:
        df = add_technical_indicators(df)
        df['Prediction'] = df['Close'].shift(-1)
        df.dropna(inplace=True)
    
        feature_columns = ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]
        X = df[feature_columns].values
        y = df['Prediction'].values

        if model_name == 'LSTM':
            scaler = MinMaxScaler(feature_range=(0, 1))
            X = scaler.fit_transform(X)
            y = scaler.fit_transform(y.reshape(-1, 1))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
            X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
            model = create_lstm_model((X_train.shape[1], 1))
            model.fit(X_train, y_train, batch_size=32, epochs=50)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            ModelClass = AVAILABLE_MODELS.get(model_name)
            if not ModelClass:
                raise ValueError(f"Model {model_name} is not supported.")

            model = ModelClass()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)

        if model_name != 'LSTM':
            with open(model_file, 'wb') as f:
                pickle.dump((model, mse), f)
    
    return model, mse, scaler

# Step 3: Plotting and GUI Interaction
def plot_data(df, predictions, stock_symbol, model_name):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index[-len(predictions):], predictions, label='Predicted Prices', color='orange')
    plt.plot(df.index[-len(predictions):], df['Close'].tail(len(predictions)), label='Actual Prices', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.title(f'{model_name} Prediction vs Actual Prices for {stock_symbol.upper()}')
    plt.show()

# Define show_historical_data function
def show_historical_data():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        df = scrape_data(stock_symbol)
        historical_data = df.tail(30)
        messagebox.showinfo("Historical Data", historical_data.to_string())
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Additional Features

def predict_stock_price():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        if not stock_symbol:
            raise ValueError("Please enter a valid stock symbol.")
        
        model_name = model_var.get()
        if model_name not in AVAILABLE_MODELS:
            raise ValueError("Selected model is not supported.")
        
        df = scrape_data(stock_symbol)
        df.name = stock_symbol
        model, mse, scaler = train_model(df, model_name)
        
        latest_features = df[['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]].tail(1)
        
        # Reshape data for LSTM model prediction
        if model_name == "LSTM":
            latest_features = scaler.transform(latest_features)
            latest_features = latest_features.reshape((latest_features.shape[0], latest_features.shape[1], 1))
        
        predicted_price = model.predict(latest_features)[0]
        
        # Convert the predicted price to a scalar
        if isinstance(predicted_price, np.ndarray):
            predicted_price = predicted_price.item()

        # If LSTM, inverse scale the prediction
        if model_name == "LSTM":
            predicted_price = scaler.inverse_transform([[predicted_price]])[0][0]

        result_message = f"Predicted Next Day Close Price: ${predicted_price:.2f}"
        if mse is not None:
            result_message += f"\nModel Mean Squared Error (MSE): {mse:.4f}"
        
        messagebox.showinfo("Stock Price Prediction", result_message)
        
        plot_features = df[['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]].tail(30)
        
        # Reshape data for LSTM model prediction
        if model_name == "LSTM":
            plot_features = scaler.transform(plot_features)
            plot_features = plot_features.reshape((plot_features.shape[0], plot_features.shape[1], 1))
        
        plot_predictions = model.predict(plot_features)
        
        if model_name == "LSTM":
            plot_predictions = scaler.inverse_transform(plot_predictions).flatten()

        plot_data(df, plot_predictions, stock_symbol, model_name)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_prediction_to_file():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        if not stock_symbol:
            raise ValueError("Please enter a valid stock symbol.")
        
        model_name = model_var.get()
        if model_name not in AVAILABLE_MODELS:
            raise ValueError("Selected model is not supported.")
        
        df = scrape_data(stock_symbol)
        df.name = stock_symbol
        model, mse, scaler = train_model(df, model_name)
        
        latest_features = df[['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]].tail(1)
        
        # Reshape data for LSTM model prediction
        if model_name == "LSTM":
            latest_features = scaler.transform(latest_features)
            latest_features = latest_features.reshape((latest_features.shape[0], latest_features.shape[1], 1))
        
        predicted_price = model.predict(latest_features)[0]
        
        # Convert the predicted price to a scalar
        if isinstance(predicted_price, np.ndarray):
            predicted_price = predicted_price.item()
        
        # If LSTM, inverse scale the prediction
        if model_name == "LSTM":
            predicted_price = scaler.inverse_transform([[predicted_price]])[0][0]

        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if save_path:
            df.tail(30).to_csv(save_path)
            with open(save_path, 'a') as f:
                f.write(f"\nPredicted Next Day Close Price: ${predicted_price:.2f}\nModel Mean Squared Error (MSE): {mse:.4f}")
            messagebox.showinfo("Save Prediction", "Prediction and data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def compare_models():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        if not stock_symbol:
            raise ValueError("Please enter a valid stock symbol.")
        
        df = scrape_data(stock_symbol)
        df.name = stock_symbol
        
        results = {}
        for model_name in AVAILABLE_MODELS.keys():
            model, mse, _ = train_model(df, model_name)
            results[model_name] = mse
        
        result_message = "\n".join([f"{model}: MSE = {mse:.4f}" for model, mse in results.items()])
        messagebox.showinfo("Model Comparison", result_message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_full_data():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        if not stock_symbol:
            raise ValueError("Please enter a valid stock symbol.")
        
        df = scrape_data(stock_symbol)
        
        # Create a new window to display the data
        data_window = tk.Toplevel(root)
        data_window.title(f"Full Historical Data for {stock_symbol.upper()}")
        
        # Create a text widget to display the data
        text = tk.Text(data_window, wrap="none")
        text.insert(tk.END, df.to_string())
        text.pack(expand=True, fill=tk.BOTH)
        
        # Add scrollbars
        x_scroll = tk.Scrollbar(data_window, orient=tk.HORIZONTAL, command=text.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        text['xscrollcommand'] = x_scroll.set
        
        y_scroll = tk.Scrollbar(data_window, orient=tk.VERTICAL, command=text.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text['yscrollcommand'] = y_scroll.set
    except Exception as e:
        messagebox.showerror("Error", str(e))

def customize_date_range():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        if not stock_symbol:
            raise ValueError("Please enter a valid stock symbol.")
        
        # Prompt user for start and end dates
        start_date = simpledialog.askstring("Input", "Enter start date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Input", "Enter end date (YYYY-MM-DD):")
        
        if start_date and end_date:
            df = yf.download(stock_symbol, start=start_date, end=end_date)
            if df.empty:
                raise ValueError("No data found for this date range.")
            
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            
            # Display the fetched data
            data_window = tk.Toplevel(root)
            data_window.title(f"Data for {stock_symbol.upper()} from {start_date} to {end_date}")
            
            # Create a text widget to display the data
            text = tk.Text(data_window, wrap="none")
            text.insert(tk.END, df.to_string())
            text.pack(expand=True, fill=tk.BOTH)
            
            # Add scrollbars
            x_scroll = tk.Scrollbar(data_window, orient=tk.HORIZONTAL, command=text.xview)
            x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            text['xscrollcommand'] = x_scroll.set
            
            y_scroll = tk.Scrollbar(data_window, orient=tk.VERTICAL, command=text.yview)
            y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            text['yscrollcommand'] = y_scroll.set
    except Exception as e:
        messagebox.showerror("Error", str(e))

def reset_application():
    stock_symbol_var.set("AAPL")
    model_var.set("Random Forest")
    messagebox.showinfo("Reset", "Application has been reset!")

# GUI Setup
def setup_gui():
    global stock_symbol_var, model_var, root
    
    # Create the main application window (root)
    root = tk.Tk()
    root.title("Machine Learning Market Predictor")

    # Initialize the tkinter variables after root is created
    stock_symbol_var = tk.StringVar(value="AAPL")
    model_var = tk.StringVar(value="Random Forest")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(padx=10, pady=10)

    # Stock Symbol Selection
    label_stock = tk.Label(frame, text="Enter Stock Symbol (e.g., AAPL):")
    label_stock.pack(anchor='w')

    stock_entry = tk.Entry(frame, textvariable=stock_symbol_var, width=30)
    stock_entry.pack(pady=(0, 10))

    # Model Selection
    label_model = tk.Label(frame, text="Select Prediction Model:")
    label_model.pack(anchor='w')

    model_dropdown = ttk.Combobox(frame, textvariable=model_var, values=["Linear Regression", "Random Forest", "LSTM"], state="readonly", width=28)
    model_dropdown.pack(pady=(0, 10))

    # Predict Button
    button_predict = tk.Button(frame, text="Predict", command=predict_stock_price, width=20, bg='green', fg='white')
    button_predict.pack(pady=(0, 5))

    # Show Historical Data Button
    button_history = tk.Button(frame, text="Show Last 30 Days", command=show_historical_data, width=20, bg='blue', fg='white')
    button_history.pack()

    # Save Prediction Button
    button_save = tk.Button(frame, text="Save Prediction", command=save_prediction_to_file, width=20, bg='purple', fg='white')
    button_save.pack(pady=(0, 5))

    # Compare Models Button
    button_compare = tk.Button(frame, text="Compare Models", command=compare_models, width=20, bg='orange', fg='white')
    button_compare.pack(pady=(0, 5))

    # View Full Data Button
    button_view_data = tk.Button(frame, text="View Full Data", command=view_full_data, width=20, bg='grey', fg='white')
    button_view_data.pack(pady=(0, 5))

    # Customize Date Range Button
    button_date_range = tk.Button(frame, text="Customize Date Range", command=customize_date_range, width=20, bg='brown', fg='white')
    button_date_range.pack(pady=(0, 5))

       # Reset Button
    button_reset = tk.Button(frame, text="Reset", command=reset_application, width=20, bg='red', fg='white')
    button_reset.pack(pady=(0, 5))

    # Start the Tkinter main loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    setup_gui()
