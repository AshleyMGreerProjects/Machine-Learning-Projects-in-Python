import sqlite3
import pandas as pd
from fpdf import FPDF
from tkinter import messagebox, filedialog

def export_to_csv():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            conn = sqlite3.connect('risk_assessment.db')
            df = pd.read_sql_query("SELECT * FROM risk_assessments", conn)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export to CSV", "Export successful!")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred during export: {e}")
    finally:
        if conn:
            conn.close()

def generate_pdf_report():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            conn = sqlite3.connect('risk_assessment.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM risk_assessments")
            assessments = cursor.fetchall()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="Cybersecurity Risk Assessment Report", ln=True, align='C')
            pdf.ln(10)

            for assessment in assessments:
                pdf.multi_cell(0, 10, txt=f"Threat: {assessment[1]}, Likelihood: {assessment[2]}, Impact: {assessment[3]}, Exposure: {assessment[4]}, Mitigation: {assessment[5]}, "
                                          f"Asset Value: {assessment[6]}, Threat Intel: {assessment[7]}, Vulnerability Severity: {assessment[8]}, "
                                          f"Control Effectiveness: {assessment[9]}, RTO: {assessment[10]}, Risk Score: {assessment[11]:.2f}, Risk Level: {assessment[12]}")
                pdf.ln(5)

            pdf.output(file_path)
            messagebox.showinfo("PDF Report", "PDF report generated successfully!")
    except Exception as e:
        messagebox.showerror("PDF Generation Error", f"An error occurred while generating the PDF report: {e}")
    finally:
        if conn:
            conn.close()

def clear_list(risk_list):
    risk_list.delete(0, END)
