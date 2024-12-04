# tabs/PatientFormTab.py
import tkinter as tk
from tkinter import ttk, messagebox as mb
from tkcalendar import DateEntry
import pandas as pd
import json
import os
import sys
from cryptography.fernet import Fernet
from fpdf import FPDF

"""
- Tab containing a form to collect patient information and make predictions.
- Allows saving the patient data and prediction result to an encrypted file.
- Uses the model to make predictions based on the input data.
"""
class PatientFormTab:
    # Constructor
    def __init__(self, parent, model):
        self.frame = ttk.Frame(parent)
        self.model = model 
        self.prediction_result = None
        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)
        self.create_widgets()

    # Find file using relative path
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Get key
    def load_key(self):
        key_path = self.resource_path("secret.key")
        try:
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
            return key
        except FileNotFoundError:
            mb.showerror("Error", "Encryption key file 'secret.key' not found.")
            raise
        except Exception as e:
            mb.showerror("Error", f"An unexpected error occurred while loading the key: {e}")
            raise
    
    # Make widgets
    def create_widgets(self):
        patient_frame = ttk.LabelFrame(self.frame, text="Patient Information", padding=(20, 10))
        patient_frame.pack(fill="x", padx=20, pady=10)

        medical_frame = ttk.LabelFrame(self.frame, text="Medical Data", padding=(20, 10))
        medical_frame.pack(fill="x", padx=20, pady=10)

        # Define labels and values
        self.fields = [
            ("First Name:", "entry"),
            ("Last Name:", "entry"),
            ("Date of Birth:", "date"),  # Change to 'date' type
            ("Age:", "entry"),
            ("Sex:", ["Male", "Female"]),
            ("Chest Pain Type (0-3):", ["0", "1", "2", "3"]),
            ("Resting Blood Pressure (mmHg):", "entry"),
            ("Serum Cholesterol (mg/dL):", "entry"),
            ("Fasting Blood Sugar > 120 mg/dL:", ["Yes", "No"]),
            ("Resting ECG:", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"]),
            ("Max Heart Rate (BPM):", "entry"),
            ("Exercise Induced Angina:", ["Yes", "No"]),
            ("ST Depression:", "entry"),
            ("Slope of Peak Exercise ST Segment:", ["Upsloping", "Flat", "Downsloping"]),
            ("Number of Major Vessels:", ["0", "1", "2", "3"]),
            ("Thalassemia:", ["Normal", "Fixed Defect", "Reversible Defect"]),
        ]

        # Dictionary to store widget references
        self.widgets = {}

        # Determine width of longest label
        max_label_length = max(len(label) for label, _ in self.fields)
        field_width = max_label_length + 5  

        # Create patient information fields
        for i, (label, value) in enumerate(self.fields):
            if label in ["First Name:", "Last Name:", "Date of Birth:", "Age:"]:
                parent_frame = patient_frame
                row_index = i  
            else:
                parent_frame = medical_frame
                row_index = i - 4
            
            # Add label and widget to frame
            ttk.Label(parent_frame, text=label).grid(row=row_index, column=0, sticky="w", pady=5)
            if isinstance(value, list): 
                widget = ttk.Combobox(
                    parent_frame,
                    values=value,
                    width=field_width,
                    state="readonly"
                )
            elif value == "date": 
                widget = DateEntry(
                    parent_frame,
                    width=field_width - 2,
                    background='darkblue',
                    foreground='white',
                    borderwidth=2,
                    date_pattern='y-mm-dd' 
                )
            else: 
                widget = ttk.Entry(parent_frame, width=field_width)
            widget.grid(row=row_index, column=1, pady=5)
            self.widgets[label] = widget

        # Button frame
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=20)

        # Submit button
        tk.Button(
            button_frame,
            text="Submit",
            command=self.submit_info,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
        ).pack(side="left", padx=10)

        # Save Report button
        tk.Button(
            button_frame,
            text="Save Report",
            command=self.save_report,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
        ).pack(side="left", padx=10)

    # Send patient info to json
    def submit_info(self):
        # Check if all fields are filled
        for label, widget in self.widgets.items():
            if isinstance(widget, ttk.Combobox) and not widget.get():
                mb.showerror("Error", f"Please fill in the {label.lower()}")
                return
            elif isinstance(widget, (ttk.Entry, DateEntry)) and not widget.get().strip():
                mb.showerror("Error", f"Please fill in the {label.lower()}")
                return

        # Process data
        data = {label.strip(':'): widget.get() for label, widget in self.widgets.items()}
        print("Collected Data:", data)  # Debugging line

        # Preprocess data to match model data
        try:
            input_data = self.preprocess_data(data)
            print("Preprocessed Data:", input_data)  # Debugging line
            prediction = self.model.predict(input_data)
            result = prediction[0]

            # Store prediction
            self.prediction_result = result

            # Display result
            if result == 0:
                mb.showinfo("Result", "NO signs of heart disease detected.")
            else:
                mb.showinfo("Result", "Signs of heart disease detected.")
        except Exception as e:
            mb.showerror("Error", f"An error occurred during calculations: {e}")

    # Preprocess data
    def preprocess_data(self, data):
        # Map user input to model value
        mapping = {
            "Sex": {"Male": 1, "Female": 0},
            "Age": lambda x: float(x),
            "Serum Cholesterol (mg/dL)": lambda x: float(x),
            "Max Heart Rate (BPM)": lambda x: float(x),
            "ST Depression": lambda x: float(x),
            "Fasting Blood Sugar > 120 mg/dL": {"Yes": 1, "No": 0},
            "Exercise Induced Angina": {"Yes": 1, "No": 0},
            "Chest Pain Type (0-3)": {"0": 0, "1": 1, "2": 2, "3": 3},
            "Resting ECG": {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2},
            "Slope of Peak Exercise ST Segment": {"Upsloping": 0, "Flat": 1, "Downsloping": 2},
            "Number of Major Vessels": {"0": 0, "1": 1, "2": 2, "3": 3},
            "Thalassemia": {"Normal": 3, "Fixed Defect": 6, "Reversible Defect": 7},
        }

        # Map of GUI labels to feature names
        label_to_feature = {
            "Age": "age",
            "Sex": "sex",
            "Chest Pain Type (0-3)": "cp",
            "Resting Blood Pressure (mmHg)": "trestbps",
            "Serum Cholesterol (mg/dL)": "chol",
            "Fasting Blood Sugar > 120 mg/dL": "fbs",
            "Resting ECG": "restecg",
            "Max Heart Rate (BPM)": "thalach",
            "Exercise Induced Angina": "exang",
            "ST Depression": "oldpeak",
            "Slope of Peak Exercise ST Segment": "slope",
            "Number of Major Vessels": "ca",
            "Thalassemia": "thal"
        }

        # Ordered list of feature names
        feature_order = [
            "age", "sex", "cp", "trestbps", "chol",
            "fbs", "restecg", "thalach", "exang",
            "oldpeak", "slope", "ca", "thal"
        ]

        # Prepare the data
        processed_data = []

        for label in label_to_feature:
            feature = label_to_feature[label]
            if label in data:
                value = data[label]
                if label in mapping:
                    if isinstance(mapping[label], dict):
                        # For dictionary mappings
                        value = mapping[label].get(value)
                    elif callable(mapping[label]):
                        # For callable mappings (e.g., lambda functions)
                        try:
                            value = mapping[label](value)
                        except Exception as e:
                            raise ValueError(f"Error processing {label}: {e}")
                    else:
                        raise ValueError(f"Invalid mapping type for {label}")
                    
                    if value is None:
                        raise ValueError(f"Invalid value for {label}")
                else:
                    # If no mapping is defined, attempt to convert to float
                    try:
                        value = float(value)
                    except ValueError:
                        raise ValueError(f"Invalid input for {label}: must be a number.")
                
                processed_data.append(value)
            else:
                raise ValueError(f"Missing value for {label}")

        # Create a pandas DataFrame with the collected data
        input_df = pd.DataFrame([processed_data], columns=feature_order)
        return input_df

    # Save report
    def save_report(self):
        # Check if prediction exists
        if self.prediction_result is None:
            mb.showwarning("Warning", "Please submit the form before saving.")
            return

        # Get data
        data = {label.strip(':'): widget.get() for label, widget in self.widgets.items()}

        # Add prediction result
        if self.prediction_result == 0:
            result_text = "NO signs of heart disease detected."
        else:
            result_text = "Signs of heart disease detected."

        data["Prediction Result"] = result_text

        # Create hashmap key with first name, last name, and DOB
        first_name = data.get("First Name", "").strip()
        last_name = data.get("Last Name", "").strip()
        date_of_birth = data.get("Date of Birth", "").strip()

        if not first_name or not last_name or not date_of_birth:
            mb.showerror("Error", "First Name, Last Name, and Date of Birth are required to save the report.")
            return

        key = f"{first_name}_{last_name}_{date_of_birth}"

        # Load and decrypt file
        reports = {}
        report_path = self.resource_path("hdisrep.json")
        if os.path.exists(report_path):
            try:
                with open(report_path, "rb") as f:
                    encrypted_data = f.read()
                    if encrypted_data:
                        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                        reports = json.loads(decrypted_data.decode('utf-8'))
                    else:
                        reports = {}
            except Exception as e:
                # Handle error
                response = mb.askyesno("Error", f"Error decrypting '{report_path}': {e}\n\nOverwrite with new data?")
                if response:
                    reports = {}
                else:
                    return
        else:
            reports = {}

        # Add or update patient's data
        reports[key] = data

        # Save and encrypt updated data
        try:
            updated_data = json.dumps(reports).encode('utf-8')
            encrypted_data = self.cipher_suite.encrypt(updated_data)
            with open(report_path, "wb") as f:
                f.write(encrypted_data)
            mb.showinfo("Success", "Patient report saved successfully.")
        except Exception as e:
            mb.showerror("Error", f"An error occurred while saving the report: {e}")
