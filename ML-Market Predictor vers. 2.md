**Project Name:** Machine Learning Market Predictor - Version 2

**Author:** Ashley M. Greer, Jr

**Project Overview:**

This advanced version of the Machine Learning Market Predictor builds upon the first version by introducing a Long Short-Term Memory (LSTM) neural network for time series forecasting. The script is designed to predict stock prices using both traditional machine learning models and deep learning techniques. It includes feature engineering, model training, and a graphical user interface for ease of use.

**Features:**

- **Data Scraping:** Fetches historical stock data using the `yfinance` API, with options to cache data locally.
- **Advanced Feature Engineering:** Includes calculations for Moving Averages, RSI, MACD, and lagged features to enhance predictive accuracy.
- **LSTM Model:** Implements an LSTM neural network for capturing temporal dependencies in stock price data, alongside Linear Regression and Random Forest.
- **Visualization:** Generates detailed plots comparing predicted prices with actual prices, allowing users to visually assess model performance.
- **Model Comparison:** Compares the performance of different models (Linear Regression, Random Forest, LSTM) using Mean Squared Error (MSE).
- **User Interface:** A Tkinter-based GUI allows users to select models, fetch data, and visualize predictions with ease.

**Technologies Used:**

- **Python:** The core language for development.
- **Scikit-Learn:** Used for traditional machine learning models.
- **TensorFlow/Keras:** Used for building and training the LSTM model.
- **Matplotlib:** Used for visualizing stock price predictions.
- **yfinance:** API for downloading financial data.
- **Tkinter:** Provides a user-friendly graphical interface.

**Usage:**

- **Fetch Data:** Use the GUI to enter a stock symbol and fetch historical data.
- **Train Models:** Choose between Linear Regression, Random Forest, or LSTM, and train the model on the fetched data.
- **Visualize Predictions:** Compare the model’s predictions against actual prices using the visualization feature.
- **Compare Models:** Evaluate different models to find the one with the best performance based on MSE.

**Future Enhancements:**

- **Hybrid Models:** Explore the development of hybrid models that combine the strengths of both traditional machine learning and deep learning techniques.
- **Automated Hyperparameter Tuning:** Integrate automated hyperparameter tuning to optimize model performance.

**License:** This project is licensed under the MIT License.