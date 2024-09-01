
**Project Name:** Machine Learning Market Predictor - Version 1

**Author:** Ashley M. Greer, Jr

**Project Overview:**

This project is a Python-based tool designed to predict stock prices using machine learning models. The primary models used include Linear Regression and Random Forest. The script scrapes financial data from Yahoo Finance, performs feature engineering with various technical indicators, and provides predictions for future stock prices. It also includes a comparison feature to evaluate model performance and a user-friendly GUI for interaction.

**Features:**

- **Data Scraping:** Retrieves historical stock data from Yahoo Finance using the `yfinance` API.
- **Feature Engineering:** Calculates technical indicators like Moving Averages, RSI, and MACD to enhance model accuracy.
- **Model Training:** Supports Linear Regression and Random Forest models, allowing users to train and test predictions.
- **Visualization:** Generates and displays graphs comparing predicted stock prices with actual historical prices.
- **Model Comparison:** Allows users to compare the performance of different models using Mean Squared Error (MSE) as a metric.
- **GUI Interface:** Provides a Tkinter-based interface for easy interaction, including options to select stock symbols, choose models, and visualize results.

**Technologies Used:**

- **Python:** The core language for scripting.
- **Scikit-Learn:** Used for implementing machine learning models like Linear Regression and Random Forest.
- **Matplotlib:** Used for visualizing stock price predictions.
- **yfinance:** API for fetching stock data from Yahoo Finance.
- **Tkinter:** Provides a simple graphical interface for the tool.


**Usage:**

- **Data Scraping:** Enter the stock symbol and click "Fetch Data" to retrieve the latest historical data.
- **Train Model:** Select a model (Linear Regression or Random Forest) and click "Train" to build the predictive model.
- **Visualize Results:** After training, click "Visualize" to see the comparison between predicted and actual stock prices.
- **Compare Models:** Use the "Compare Models" feature to evaluate the accuracy of different models.

**Future Enhancements:**

- **Additional Models:** Consider adding more machine learning models, such as Support Vector Machines or Gradient Boosting, for enhanced prediction capabilities.
- **Automated Model Selection:** Implement a feature that automatically selects the best-performing model based on past performance.

**License:** This project is licensed under the MIT License.

