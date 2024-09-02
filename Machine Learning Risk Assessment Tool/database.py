import sqlite3
import csv
from fpdf import FPDF
from tkinter import messagebox

def setup_database():
    try:
        conn = sqlite3.connect('risk_assessment.db')
        cursor = conn.cursor()
        
        # Create the risk assessments table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                threat TEXT,
                likelihood INTEGER,
                impact INTEGER,
                exposure INTEGER,
                mitigation INTEGER,
                asset_value INTEGER,
                threat_intel INTEGER,
                vulnerability_severity INTEGER,
                control_effectiveness INTEGER,
                rto INTEGER,
                risk_score REAL,
                risk_level TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while setting up the database: {e}")
    finally:
        conn.close()

def export_to_csv():
    try:
        conn = sqlite3.connect('risk_assessment.db')
        cursor = conn.cursor()
        
        # Fetch all data from the risk_assessments table
        cursor.execute("SELECT * FROM risk_assessments")
        rows = cursor.fetchall()
        
        if not rows:
            messagebox.showwarning("No Data", "No data available to export.")
            return

        # Ask the user where to save the CSV file
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([description[0] for description in cursor.description])  # Write headers
                writer.writerows(rows)  # Write data
            messagebox.showinfo("Export Successful", f"Data successfully exported to {file_path}")
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while exporting data: {e}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

def generate_pdf_report():
    try:
        conn = sqlite3.connect('risk_assessment.db')
        cursor = conn.cursor()

        # Fetch all data from the risk_assessments table
        cursor.execute("SELECT * FROM risk_assessments")
        rows = cursor.fetchall()

        if not rows:
            messagebox.showwarning("No Data", "No data available to generate a PDF report.")
            return

        # Ask the user where to save the PDF file
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Risk Assessment Report", ln=True, align="C")

            pdf.ln(10)

            col_width = pdf.w / 4.5
            row_height = pdf.font_size

            # Add headers
            headers = [description[0] for description in cursor.description]
            for header in headers:
                pdf.cell(col_width, row_height * 2, txt=header, border=1)

            pdf.ln(row_height * 2)

            # Add data rows
            for row in rows:
                for item in row:
                    pdf.cell(col_width, row_height * 2, txt=str(item), border=1)
                pdf.ln(row_height * 2)

            pdf.output(file_path)
            messagebox.showinfo("Report Generated", f"PDF report successfully generated at {file_path}")
        
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while generating the report: {e}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
