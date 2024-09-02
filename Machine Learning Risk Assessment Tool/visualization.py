import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox

def visualize_risks():
    try:
        conn = sqlite3.connect('risk_assessment.db')
        df = pd.read_sql_query("SELECT likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto, risk_score, risk_level FROM risk_assessments", conn)
        
        if df.empty:
            messagebox.showwarning("Visualization Error", "No data available to visualize.")
            return

        # Risk level distribution
        plt.figure(figsize=(10, 6))
        risk_level_counts = df['risk_level'].value_counts()
        risk_level_counts.plot(kind='bar', color=['green', 'orange', 'red'], alpha=0.7)
        plt.title("Risk Levels Distribution")
        plt.xlabel("Risk Level")
        plt.ylabel("Frequency")
        plt.show()

        # Scatter plot for Likelihood vs Impact with risk score as color
        plt.figure(figsize=(10, 6))
        plt.scatter(df['likelihood'], df['impact'], c=df['risk_score'], cmap='viridis', alpha=0.6, edgecolors='w', s=100)
        plt.colorbar(label='Risk Score')
        plt.title("Likelihood vs. Impact")
        plt.xlabel("Likelihood")
        plt.ylabel("Impact")
        plt.show()

        # Heatmap for threat intelligence vs vulnerability severity
        plt.figure(figsize=(10, 6))
        plt.scatter(df['threat_intel'], df['vulnerability_severity'], c=df['risk_score'], cmap='coolwarm', alpha=0.6, edgecolors='w', s=100)
        plt.colorbar(label='Risk Score')
        plt.title("Threat Intelligence vs. Vulnerability Severity")
        plt.xlabel("Threat Intelligence")
        plt.ylabel("Vulnerability Severity")
        plt.show()

    except Exception as e:
        messagebox.showerror("Visualization Error", f"An error occurred during visualization: {e}")
    finally:
        if conn:
            conn.close()

def visualize_risk_scoring_chart():
    try:
        conn = sqlite3.connect('risk_assessment.db')
        df = pd.read_sql_query("SELECT risk_score FROM risk_assessments", conn)
        
        if df.empty:
            messagebox.showwarning("Visualization Error", "No data available to visualize.")
            return

        # Plotting the risk scoring chart as a histogram
        plt.figure(figsize=(10, 6))
        plt.hist(df['risk_score'], bins=20, color='blue', alpha=0.7)
        plt.title("Risk Scoring Distribution")
        plt.xlabel("Risk Score")
        plt.ylabel("Frequency")
        plt.show()
    except Exception as e:
        messagebox.showerror("Visualization Error", f"An error occurred during visualization: {e}")
    finally:
        if conn:
            conn.close()