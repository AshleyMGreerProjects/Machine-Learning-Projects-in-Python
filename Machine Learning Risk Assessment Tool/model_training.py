import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from tkinter import messagebox

def train_models():
    try:
        conn = sqlite3.connect('risk_assessment.db')
        df = pd.read_sql_query("SELECT likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto, risk_score FROM risk_assessments", conn)
        
        if df.empty:
            messagebox.showwarning("Training Error", "No data available to train models.")
            return

        X = df[['likelihood', 'impact', 'exposure', 'mitigation', 'asset_value', 'threat_intel', 'vulnerability_severity', 'control_effectiveness', 'rto']]
        y = df['risk_score']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Linear Regression
        global lr_model
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)

        # Train Random Forest
        global rf_model
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)

        # Evaluate models
        lr_predictions = lr_model.predict(X_test)
        rf_predictions = rf_model.predict(X_test)

        lr_mae = mean_absolute_error(y_test, lr_predictions)
        lr_r2 = r2_score(y_test, lr_predictions)

        rf_mae = mean_absolute_error(y_test, rf_predictions)
        rf_r2 = r2_score(y_test, rf_predictions)

        messagebox.showinfo("Training Complete", f"Models trained successfully!\n\nLinear Regression - MAE: {lr_mae:.2f}, R2: {lr_r2:.2f}\n"
                                                 f"Random Forest - MAE: {rf_mae:.2f}, R2: {rf_r2:.2f}")
    except ValueError as e:
        messagebox.showerror("Training Error", f"An error occurred during model training: {e}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

def predict_risk_score(model_name, likelihood_var, impact_var, exposure_var, mitigation_var, asset_value_var, threat_intel_var, vulnerability_severity_var, control_effectiveness_var, rto_var):
    try:
        likelihood = int(likelihood_var.get())
        impact = int(impact_var.get())
        exposure = int(exposure_var.get())
        mitigation = int(mitigation_var.get())
        asset_value = int(asset_value_var.get())
        threat_intel = int(threat_intel_var.get())
        vulnerability_severity = int(vulnerability_severity_var.get())
        control_effectiveness = int(control_effectiveness_var.get())
        rto = int(rto_var.get())

        features = [[likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto]]

        if model_name == 'Linear Regression':
            prediction = lr_model.predict(features)[0]
        else:
            prediction = rf_model.predict(features)[0]

        return prediction
    except NameError:
        messagebox.showwarning("Prediction Error", "Models have not been trained yet.")
        return None
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid input! Please enter numerical values.")
        return None
    except Exception as e:
        messagebox.showerror("Prediction Error", f"An error occurred during prediction: {e}")
        return None