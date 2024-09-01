# Machine Learning SIEM Script

**Author:** Ashley M. Greer, Jr

## Overview

The **Machine Learning SIEM Script** is a Python-based project designed to enhance network security by integrating machine learning into a Security Information and Event Management (SIEM) system. This system monitors network traffic, detects anomalies using machine learning algorithms, and provides real-time alerts for potential security threats. The script includes features for log management, model retraining, and data visualization, making it an effective tool for proactive network defense.

## Features

### 1. **Real-Time Network Monitoring**
   - **Description:** Continuously monitors network traffic and logs events for further analysis.
   - **Benefit:** Helps identify unusual activities as they occur, allowing for prompt responses.

### 2. **Anomaly Detection**
   - **Description:** Utilizes the Isolation Forest algorithm to detect anomalies in network traffic data. The model is capable of identifying outliers that may signify security breaches.
   - **Benefit:** Provides a robust method for detecting potential security threats in real-time.

### 3. **Log Management**
   - **Description:** Efficiently manages and stores logs, making it easier to access and analyze historical data.
   - **Benefit:** Ensures that all network activities are recorded for auditing and forensic purposes.

### 4. **Real-Time Alerts**
   - **Description:** Automatically generates alerts when an anomaly is detected, notifying the security team for immediate action.
   - **Benefit:** Enhances the responsiveness of the security team to potential threats.

### 5. **Data Visualization**
   - **Description:** Provides tools for visualizing network traffic data and anomaly detection results, helping to identify patterns and trends.
   - **Benefit:** Simplifies the analysis of network traffic and aids in identifying recurring issues or potential vulnerabilities.

### 6. **Model Retraining**
   - **Description:** Supports the retraining of the anomaly detection model as new data becomes available, ensuring that the model adapts to evolving network conditions.
   - **Benefit:** Maintains the accuracy and relevance of the anomaly detection model over time.

## Libraries Used

### 1. **Python**
   - **Description:** Python is the primary programming language used for this project, known for its simplicity and extensive library support.
   - **Usage:** All the core logic, including data processing, machine learning, and network monitoring, is implemented in Python.

### 2. **Scikit-Learn**
   - **Description:** Scikit-Learn is a powerful machine learning library in Python that provides simple and efficient tools for data mining and data analysis.
   - **Usage:** The Isolation Forest algorithm, which is used for anomaly detection, is implemented using Scikit-Learn. The library also provides tools for model training, evaluation, and validation.

### 3. **Matplotlib**
   - **Description:** Matplotlib is a plotting library in Python used for creating static, animated, and interactive visualizations.
   - **Usage:** Matplotlib is used to generate visualizations of network traffic data and anomaly detection results, helping users to easily interpret the findings.

### 4. **Tkinter**
   - **Description:** Tkinter is the standard GUI library in Python. It provides a fast and easy way to create graphical user interfaces.
   - **Usage:** The Tkinter library is used to build the graphical user interface (GUI) for the SIEM system, allowing users to interact with the tool through a visual interface.

### 5. **Logging**
   - **Description:** The logging module in Python is used for tracking events that happen when software runs. It is crucial for debugging and running diagnostics.
   - **Usage:** Logging is used throughout the script to keep track of various operations, errors, and warnings, making it easier to diagnose issues and understand the system's performance.

## Usage

### Starting the SIEM System
- Launch the application using the GUI to begin monitoring network traffic in real-time.

### Viewing Logs
- Access the log management system through the GUI to view and analyze historical network activity.

### Visualizing Data
- Use the built-in visualization tools to plot network traffic data and identify patterns or trends.

### Retraining the Model
- As new data is collected, retrain the anomaly detection model to ensure it continues to accurately identify potential threats.

### Receiving Alerts
- The system will automatically generate alerts when an anomaly is detected, notifying the user through the GUI.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
