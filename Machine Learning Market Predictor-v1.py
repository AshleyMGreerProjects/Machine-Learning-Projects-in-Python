import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import yfinance as yf

# Directories for caching data and saving models
CACHE_DIR = "cache"
MODEL_DIR = "models"
AVAILABLE_MODELS = {
    "Linear Regression": LinearRegression,
    "Random Forest": RandomForestRegressor
}

# Ensure cache and model directories exist
for directory in [CACHE_DIR, MODEL_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Step 1: Fetch Financial Data using yfinance
def scrape_data(stock_symbol):
    """
    Fetch historical stock data using yfinance.

    Parameters:
    - stock_symbol: The stock symbol to fetch data for (e.g., 'AAPL').

    Returns:
    - df: DataFrame containing the historical stock data.
    """
    cache_file = os.path.join(CACHE_DIR, f"{stock_symbol}.csv")
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file, index_col='Date', parse_dates=True)
    else:
        # Fetch data for the past year
        df = yf.download(stock_symbol, period="1y")
        
        if df.empty:
            raise ValueError("No data found for this stock symbol.")
        
        # Ensure the Date is the index
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)

        # Save to cache
        df.to_csv(cache_file)
    
    return df

# Step 1a: Feature Engineering
def add_technical_indicators(df):
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['RSI'] = compute_RSI(df)
    df['MACD'], df['Signal'] = compute_MACD(df)
    for lag in range(1, 6):
        df[f'Close_lag_{lag}'] = df['Close'].shift(lag)
    df.dropna(inplace=True)
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
    if os.path.exists(model_file):
        with open(model_file, 'rb') as f:
            model, mse = pickle.load(f)
    else:
        df = add_technical_indicators(df)
        df['Prediction'] = df['Close'].shift(-1)
        df.dropna(inplace=True)
    
        feature_columns = ['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]
        X = df[feature_columns]
        y = df['Prediction']
    
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
        ModelClass = AVAILABLE_MODELS.get(model_name)
        if not ModelClass:
            raise ValueError(f"Model {model_name} is not supported.")
    
        model = ModelClass()
        model.fit(X_train, y_train)
    
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
    
        with open(model_file, 'wb') as f:
            pickle.dump((model, mse), f)
    
    return model, mse

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

# Step 4: Enhanced GUI with Multiple Stock Support and Model Selection
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
        model, mse = train_model(df, model_name)
        
        latest_features = df[['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]].tail(1)
        predicted_price = model.predict(latest_features)[0]
        
        result_message = f"Predicted Next Day Close Price: ${predicted_price:.2f}"
        if mse is not None:
            result_message += f"\nModel Mean Squared Error (MSE): {mse:.4f}"
        
        messagebox.showinfo("Stock Price Prediction", result_message)
        
        plot_features = df[['Open', 'High', 'Low', 'Volume', 'MA5', 'MA10', 'MA20', 'RSI', 'MACD', 'Signal'] + [f'Close_lag_{lag}' for lag in range(1,6)]].tail(30)
        plot_predictions = model.predict(plot_features)
        
        plot_data(df, plot_predictions, stock_symbol, model_name)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_historical_data():
    try:
        stock_symbol = stock_symbol_var.get().strip().lower()
        if not stock_symbol:
            raise ValueError("Please enter a valid stock symbol.")
        
        df = scrape_data(stock_symbol)
        historical_data = df.tail(30)
        messagebox.showinfo("Historical Data (Last 30 Days)", historical_data.to_string())
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
def setup_gui():
    global stock_symbol_var, model_var
    
    # Create the main application window (root)
    root = tk.Tk()
    root.title("Advanced Stock Price Predictor")

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

    model_dropdown = ttk.Combobox(frame, textvariable=model_var, values=["Linear Regression", "Random Forest"], state="readonly", width=28)
    model_dropdown.pack(pady=(0, 10))

    # Predict Button
    button_predict = tk.Button(frame, text="Predict", command=predict_stock_price, width=20, bg='green', fg='white')
    button_predict.pack(pady=(0, 5))

    # Show Historical Data Button
    button_history = tk.Button(frame, text="Show Last 30 Days", command=show_historical_data, width=20, bg='blue', fg='white')
    button_history.pack()

    # Start the Tkinter main loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    setup_gui()