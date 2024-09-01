import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import random
import numpy as np
from sklearn.ensemble import IsolationForest
from joblib import load, dump
import threading
import sqlite3
import os
import socket

class SIEMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIEM System with Real-Time Data Integration")
        self.geometry("1200x800")

        # Button to start the application
        self.start_button = ttk.Button(self, text="Start Monitoring", command=self.start_application)
        self.start_button.pack(pady=20)

        # Frame placeholders for when the app starts
        self.top_frame = None
        self.bottom_frame = None

        # Default port
        self.monitor_port = 514

    def start_application(self):
        self.start_button.pack_forget()  # Remove the start button after clicking
        self.times = []
        self.event_counts = []
        self.settings = {
            'update_interval': 5000,  # in milliseconds
            'anomaly_threshold': 0.1
        }
        
        self.start_time = datetime.now()
        self.end_time = self.start_time

        self.setup_database()
        self.model = self.load_or_train_model()

        # Create UI components
        self.create_widgets()
        self.create_plot()
        self.create_alert_area()
        self.create_control_panel()

        # Start real-time data reception
        self.start_syslog_server()

        # Start updating data and UI
        self.start_update_loop()

    def setup_database(self):
        print("Setting up database...")
        self.conn = sqlite3.connect('siem_logs.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                timestamp TEXT,
                event_count INTEGER,
                message TEXT
            )
        ''')
        self.conn.commit()

    def load_or_train_model(self):
        print("Loading or training model...")
        model_file = 'isolation_forest_model.joblib'
        if os.path.exists(model_file):
            model = load(model_file)
        else:
            model = IsolationForest(contamination=self.settings['anomaly_threshold'], random_state=42)
            sample_data = np.random.rand(100, 1) * 10  # Simulate some training data
            model.fit(sample_data)
            dump(model, model_file)
        return model

    def create_widgets(self):
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        table_frame = ttk.LabelFrame(self.top_frame, text="Log Events")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('timestamp', 'event_count', 'message')
        self.log_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.log_table.heading('timestamp', text='Timestamp')
        self.log_table.heading('event_count', text='Event Count')
        self.log_table.heading('message', text='Message')
        self.log_table.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.log_table.yview)
        self.log_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_plot(self):
        plot_frame = ttk.LabelFrame(self.bottom_frame, text="Event Count Over Time")
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.line, = self.ax.plot([], [], marker='o', linestyle='-', color='b')
        
        self.ax.set_title('Log Event Counts Over Time')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Number of Events')
        plt.xticks(rotation=45)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_alert_area(self):
        alert_frame = ttk.LabelFrame(self.bottom_frame, text="Alerts")
        alert_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.alert_text = tk.Text(alert_frame, height=5, state='disabled', bg='#ffe6e6')
        self.alert_text.pack(fill=tk.BOTH, expand=True)

    def create_control_panel(self):
        control_frame = ttk.LabelFrame(self.bottom_frame, text="Controls")
        control_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Retrain Model", command=self.retrain_model).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Clear Alerts", command=self.clear_alerts).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Manual Update", command=self.manual_update).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Change Port", command=self.change_port).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(control_frame, text="Check Port", command=self.check_port_status).pack(side=tk.LEFT, padx=5, pady=5)

    def start_update_loop(self):
        self.update_data()
        self.after(self.settings['update_interval'], self.start_update_loop)

    def update_data(self):
        self.update_table_and_plot()

    def start_syslog_server(self):
        self.syslog_server_thread = threading.Thread(target=self.syslog_server_thread_func, daemon=True)
        self.syslog_server_thread.start()

    def syslog_server_thread_func(self):
        syslog_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            syslog_server.bind(("0.0.0.0", self.monitor_port))
            print(f"Syslog server started on port {self.monitor_port}")
        except PermissionError:
            messagebox.showerror("Permission Error", f"Failed to bind to port {self.monitor_port}. Try running as administrator.")
            return
        except OSError as e:
            messagebox.showerror("Port Error", f"Could not bind to port {self.monitor_port}: {str(e)}")
            return
        
        while True:
            message, _ = syslog_server.recvfrom(1024)
            message = message.decode("utf-8")
            print(f"Received syslog message: {message}")  # Debugging line
            self.process_syslog_message(message)

    def process_syslog_message(self, message):
        current_time = datetime.now()
        event_count = random.randint(1, 20)
        
        self.end_time = current_time
        
        self.cursor.execute('INSERT INTO logs (timestamp, event_count, message) VALUES (?, ?, ?)', 
                            (current_time.strftime('%Y-%m-%d %H:%M:%S'), event_count, message))
        self.conn.commit()
        
        self.times.append(current_time)
        self.event_counts.append(event_count)
        
        if len(self.times) > 50:
            self.times.pop(0)
            self.event_counts.pop(0)
        
        self.update_table_and_plot()
        self.check_for_anomalies(event_count)

    def update_table_and_plot(self):
        self.cursor.execute('SELECT * FROM logs WHERE timestamp BETWEEN ? AND ?', 
                            (self.start_time.strftime('%Y-%m-%d %H:%M:%S'), 
                             self.end_time.strftime('%Y-%m-%d %H:%M:%S')))
        records = self.cursor.fetchall()
        
        for item in self.log_table.get_children():
            self.log_table.delete(item)
        
        for record in records:
            self.log_table.insert('', tk.END, values=record)
        
        self.line.set_xdata(self.times)
        self.line.set_ydata(self.event_counts)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw_idle()

    def check_for_anomalies(self, event_count):
        data_point = np.array([[event_count]])
        prediction = self.model.predict(data_point)
        if prediction == -1:
            alert_message = f"Anomaly detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with {event_count} events."
            self.display_alert(alert_message)

    def display_alert(self, message):
        self.alert_text.config(state='normal')
        self.alert_text.insert(tk.END, message + '\n')
        self.alert_text.config(state='disabled')
        self.alert_text.see(tk.END)

    def retrain_model(self):
        self.cursor.execute('SELECT event_count FROM logs')
        data = self.cursor.fetchall()
        if data:
            event_counts = np.array(data)
            self.model = IsolationForest(contamination=self.settings['anomaly_threshold'], random_state=42)
            self.model.fit(event_counts)
            dump(self.model, 'isolation_forest_model.joblib')
            messagebox.showinfo("Retrain Model", "Model retrained successfully with current log data.")
        else:
            messagebox.showwarning("Retrain Model", "No data available for retraining.")

    def clear_alerts(self):
        self.alert_text.config(state='normal')
        self.alert_text.delete(1.0, tk.END)
        self.alert_text.config(state='disabled')

    def manual_update(self):
        self.update_data()

    def export_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', 
                                                 filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if file_path:
            self.cursor.execute('SELECT * FROM logs')
            records = self.cursor.fetchall()
            df = pd.DataFrame(records, columns=['Timestamp', 'Event Count', 'Message'])
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Logs exported successfully to {file_path}.")

    def change_update_interval(self):
        new_interval = simpledialog.askinteger("Update Interval", "Enter new update interval (in milliseconds):", 
                                               minvalue=1000, maxvalue=60000)
        if new_interval:
            self.settings['update_interval'] = new_interval
            messagebox.showinfo("Update Interval", f"Update interval set to {new_interval} milliseconds.")

    def change_anomaly_threshold(self):
        new_threshold = simpledialog.askfloat("Anomaly Threshold", "Enter new anomaly detection threshold (e.g., 0.1):", 
                                              minvalue=0.01, maxvalue=0.5)
        if new_threshold:
            self.settings['anomaly_threshold'] = new_threshold
            self.retrain_model()
            messagebox.showinfo("Anomaly Threshold", f"Anomaly detection threshold set to {new_threshold}.")

    def change_port(self):
        new_port = simpledialog.askinteger("Change Port", "Enter the new port number:", minvalue=1, maxvalue=65535)
        if new_port:
            self.monitor_port = new_port
            messagebox.showinfo("Port Changed", f"Monitoring port changed to {new_port}. Restart the server to apply changes.")
            self.restart_syslog_server()

    def restart_syslog_server(self):
        # Stop the existing server thread
        if self.syslog_server_thread.is_alive():
            self.syslog_server_thread.join(timeout=1)
        # Start a new syslog server thread with the updated port
        self.start_syslog_server()

    def check_port_status(self):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            test_socket.bind(("0.0.0.0", self.monitor_port))
            test_socket.close()
            messagebox.showinfo("Port Status", f"Port {self.monitor_port} is available for use.")
        except OSError as e:
            messagebox.showerror("Port Status", f"Port {self.monitor_port} is not available: {str(e)}")

if __name__ == "__main__":
    app = SIEMApp()
    app.mainloop()

