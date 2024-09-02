# Machine Learning OWASP Tool

## Overview

The **Machine Learning OWASP Tool** is an advanced cybersecurity risk assessment application designed to automate and enhance the process of evaluating risks in information systems. By leveraging machine learning models, this tool helps security professionals predict and assess the severity of risks associated with various vulnerabilities, particularly those outlined by the OWASP Top 300 vulnerabilities.

## Features

- **Risk Calculation**: 
  - The tool provides a detailed risk score calculation based on user inputs related to various cybersecurity parameters, such as likelihood, impact, exposure, mitigation, asset value, and more. These parameters are combined to generate a comprehensive risk score that reflects the potential severity of a given threat.
  
- **Machine Learning Models**:
  - The tool includes two machine learning models: **Linear Regression** and **Random Forest**. These models are trained on historical risk data to predict the risk score for new, unseen scenarios. The tool allows users to select and compare the performance of these models, providing insights into which model offers the best predictions for their specific use cases.
  
- **Data Visualization**:
  - The tool includes multiple visualization options that allow users to better understand the distribution of risks, the relationship between different risk factors, and the overall risk landscape. Visualizations include:
    - **Risk Level Distribution**: A bar chart showing the frequency of different risk levels (High, Medium, Low).
    - **Scatter Plots**: Illustrate the relationships between key risk parameters, such as likelihood vs. impact, with risk scores represented as colors.
    - **Risk Score Histogram**: Displays the distribution of calculated risk scores, helping users identify common risk score ranges.

- **Data Management**:
  - Users can add, store, and manage risk data through an intuitive graphical user interface (GUI). The tool also supports exporting risk data to CSV files and generating detailed PDF reports, making it easy to document and share findings.

- **User Interface**:
  - Built with `tkinter` and `ttkbootstrap`, the tool offers a modern, user-friendly interface. Users can easily navigate through the different functionalities, input risk data, visualize results, and export information.

## Detailed File Structure

The project is modular, with each component encapsulated in its own Python script. This makes it easy to maintain, extend, and integrate into other systems.

### 1. `main.py`
- **Purpose**: The entry point of the application. It initializes the GUI and ties together all other components. When executed, it provides users with access to all functionalities, including risk calculation, machine learning model training, risk prediction, data visualization, and export options.

### 2. `database.py`
- **Purpose**: Handles all database operations. It sets up the SQLite database, ensuring that all necessary tables and columns are created. It also manages the insertion and retrieval of risk data.
- **Key Functions**:
  - `setup_database()`: Initializes the SQLite database, ensuring that all required tables and columns are present.
  - `insert_risk()`: Adds a new risk entry to the database.
  - `export_to_csv()`: Exports risk data to a CSV file.
  - `generate_pdf_report()`: Generates a detailed PDF report of the risk assessment.

### 3. `risk_calculation.py`
- **Purpose**: Focuses on the core logic of risk calculation. It processes user inputs related to various risk factors and calculates a comprehensive risk score, which is then displayed in the GUI.
- **Key Functions**:
  - `calculate_risk_score()`: Computes the risk score using a complex formula that considers multiple risk parameters. It also determines the overall risk level (High, Medium, Low) based on the calculated score.
  - `add_risk()`: Combines user inputs and calculated scores to create a new risk entry, which is then stored in the database.

### 4. `model_training.py`
- **Purpose**: Responsible for training and utilizing machine learning models. This module allows users to train the included Linear Regression and Random Forest models on existing risk data and use them to predict risk scores for new scenarios.
- **Key Functions**:
  - `train_models()`: Trains both Linear Regression and Random Forest models using historical risk data. It also evaluates the performance of these models using metrics such as Mean Absolute Error (MAE) and R².
  - `predict_risk_score()`: Uses the trained models to predict the risk score for new scenarios based on user inputs.

### 5. `visualization.py`
- **Purpose**: Contains functions that generate various visualizations to help users understand the risk data. The visualizations are designed to highlight key trends, relationships, and distributions within the data.
- **Key Functions**:
  - `visualize_risks()`: Generates scatter plots and bar charts to visualize the relationships between risk factors and the distribution of risk levels.
  - `visualize_risk_scoring_chart()`: Creates a histogram that shows the distribution of risk scores across all entries.

### 6. `data_handling.py`
- **Purpose**: This module focuses on the processing and preparation of data for machine learning and visualization. It ensures that the data is clean, formatted correctly, and ready for use in model training and risk calculations.
- **Key Functions**:
  - `clean_data()`: Cleans and preprocesses the input data to ensure it is in the correct format for analysis.
  - `prepare_data_for_modeling()`: Prepares the data for machine learning by splitting it into training and testing sets.

### 7. `gui.py`
- **Purpose**: Manages the graphical user interface (GUI) of the application. It integrates all other modules and provides a user-friendly interface for interacting with the tool.
- **Key Functions**:
  - `setup_gui()`: Initializes and configures the GUI, setting up all the necessary buttons, labels, and input fields.
  - `calculate_and_display_risk_score()`: Calculates the risk score based on user inputs and displays the result in the GUI.
  - `add_risk_to_database()`: Adds the calculated risk score and user inputs to the database.
  - `train_models_via_gui()`: Allows users to train the machine learning models directly from the GUI.
  - `visualize_risks_gui()`: Triggers the visualization of risk data through the GUI.


## Dependencies

- `tkinter`
- `ttkbootstrap`
- `sqlite3`
- `pandas`
- `fpdf`
- `sklearn`
- `matplotlib`

## Contribution

This project is open to contributions! Whether you want to add new features, improve existing ones, or fix bugs, feel free to fork the repository, submit issues, and send pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.