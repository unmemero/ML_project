import tkinter as tk
from tkinter import ttk, messagebox as mb
from tkcalendar import DateEntry
import json
import os
import sys
from cryptography.fernet import Fernet
from fpdf import FPDF

"""
- Retrieves decrypted patient information from 'hdisrep.json' file.
- Displays patient information in a text box.
- Allows user to print the patient information as a PDF.
"""

class GetPatientInfoTab:

    # Constructor
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)
        self.create_widgets()
        self.patient_data = None 

    # Resolve resource path for PyInstaller
    def resource_path(self, relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Load encryption key
    def load_key(self):
        try:
            key_path = self.resource_path('secret.key')
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
            return key
        except FileNotFoundError:
            mb.showerror("Error", "Encryption key 'secret.key' not found. Please ensure it exists in the application directory.")
            raise
        except Exception as e:
            mb.showerror("Error", f"An unexpected error occurred while loading the key: {e}")
            raise

    # Widget maker for  the tab
    def create_widgets(self):
        # Patient search frame
        search_frame = ttk.LabelFrame(self.frame, text="Search Patient", padding=(20, 10))
        search_frame.pack(fill="x", padx=20, pady=10)

        # Patient info fields
        ttk.Label(search_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.first_name_entry = ttk.Entry(search_frame, width=30)
        self.first_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(search_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.last_name_entry = ttk.Entry(search_frame, width=30)
        self.last_name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(search_frame, text="Date of Birth:").grid(row=2, column=0, sticky="w", pady=5)
        self.dob_entry = DateEntry(
            search_frame,
            width=27,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='y-mm-dd' 
        )
        self.dob_entry.grid(row=2, column=1, pady=5)

        # Search Button
        tk.Button(
            search_frame,
            text="Search",
            command=self.get_patient_info,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # Patient report frame
        self.report_frame = ttk.LabelFrame(self.frame, text="Patient Report", padding=(20, 10))
        self.report_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.report_text = tk.Text(self.report_frame, wrap="word", state="disabled", width=80, height=20)
        self.report_text.pack(fill="both", expand=True)

        # Print PDF Button
        self.print_button = tk.Button(
            self.frame,
            text="Print PDF",
            command=self.print_pdf,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
            state="disabled"
        )
        self.print_button.pack(pady=10)

    # Get patient information
    def get_patient_info(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        date_of_birth = self.dob_entry.get().strip()

        # Entry validation
        if not first_name or not last_name or not date_of_birth:
            mb.showerror("Error", "Please enter the patient's first name, last name, and date of birth.")
            return

        # Create key for patient data entry in json file
        key = f"{first_name}_{last_name}_{date_of_birth}"

        # Load and decrypt reports
        try:
            hdisrep_path = self.resource_path("hdisrep.json")
            if not os.path.exists(hdisrep_path):
                mb.showerror("Error", "No patient reports found ('hdisrep.json' is missing).")
                return

            with open(hdisrep_path, "rb") as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                    reports = json.loads(decrypted_data.decode('utf-8'))
                else:
                    mb.showerror("Error", "No patient reports found in 'hdisrep.json'.")
                    return
        except Exception as e:
            mb.showerror("Error", f"An error occurred while retrieving data: {e}")
            return

        # Retrieve patient data
        if key in reports:
            self.patient_data = reports[key]
            self.display_patient_info(self.patient_data)
            self.print_button.config(state="normal")  
        else:
            mb.showerror("Error", "Patient not found.")
            self.report_text.config(state="normal")
            self.report_text.delete("1.0", tk.END)
            self.report_text.config(state="disabled")
            self.print_button.config(state="disabled")

    # Show patient information in text box
    def display_patient_info(self, data):
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)
        report_lines = ["\nPatient Report\n", "-" * 50 + "\n"]
        for key, value in data.items():
            report_lines.append(f"{key}: {value}\n")
        self.report_text.insert(tk.END, "".join(report_lines))
        self.report_text.config(state="disabled")

    # Print patient information as PDF
    def print_pdf(self):
        if self.patient_data is None:
            mb.showerror("Error", "No patient data to print.")
            return

        # Get patient data
        first_name = self.patient_data.get("First Name", "")
        last_name = self.patient_data.get("Last Name", "")
        date_of_birth = self.patient_data.get("Date of Birth", "")

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)

        # Title
        pdf.cell(0, 10, "Patient Report", ln=True, align="C")
        pdf.ln(10)

        # Set patient data in pdf
        pdf.set_font("Arial", '', 12)
        for key, value in self.patient_data.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)

        # Save PDF file
        filename = f"{first_name}_{last_name}_{date_of_birth}.pdf"
        try:
            pdf.output(filename)
            mb.showinfo("Success", f"PDF report saved as '{filename}'.")
        except Exception as e:
            mb.showerror("Error", f"An error occurred while saving the PDF: {e}")
