import sqlite3
from tkinter import messagebox

def calculate_risk_score(likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto):
    try:
        likelihood = int(likelihood)
        impact = int(impact)
        exposure = int(exposure)
        mitigation = int(mitigation)
        asset_value = int(asset_value)
        threat_intel = int(threat_intel)
        vulnerability_severity = int(vulnerability_severity)
        control_effectiveness = int(control_effectiveness)
        rto = int(rto)

        # Complex risk score calculation
        risk_score = ((likelihood * impact * exposure * asset_value * threat_intel * vulnerability_severity) / 
                      (mitigation * control_effectiveness * rto))

        # Determine the risk level
        if risk_score >= 150:
            risk_level = "High"
        elif risk_score >= 75:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return risk_score, risk_level
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid input! Please enter numerical values for all fields.")
    except ZeroDivisionError:
        messagebox.showwarning("Calculation Error", "Mitigation, Control Effectiveness, and RTO values cannot be zero.")
    except Exception as e:
        messagebox.showerror("Calculation Error", f"An unexpected error occurred: {e}")
        return None, None

def add_risk(threat, likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto):
    conn = None  # Initialize conn here
    try:
        conn = sqlite3.connect('risk_assessment.db')
        cursor = conn.cursor()

        risk_score, risk_level = calculate_risk_score(likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto)
        if risk_score is None:
            return

        cursor.execute("INSERT INTO risk_assessments (threat, likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto, risk_score, risk_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (threat, likelihood, impact, exposure, mitigation, asset_value, threat_intel, vulnerability_severity, control_effectiveness, rto, risk_score, risk_level))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while inserting data: {e}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()