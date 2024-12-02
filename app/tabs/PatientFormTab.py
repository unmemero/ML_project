# PatientFormTab.py
import tkinter as tk
from tkinter import ttk, messagebox as mb
from tkcalendar import DateEntry
import pandas as pd
import json
import os
from cryptography.fernet import Fernet

class PatientFormTab:
    """Encapsulates the patient form."""

    def __init__(self, parent, model):
        self.frame = ttk.Frame(parent)
        self.model = model  # Store the model instance
        self.prediction_result = None  # To store the prediction result
        self.create_widgets()

        # Load encryption key
        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)

    def load_key(self):
        """Load the encryption key from 'secret.key'."""
        try:
            with open('secret.key', 'rb') as key_file:
                key = key_file.read()
            return key
        except FileNotFoundError:
            mb.showerror("Error", "Encryption key file 'secret.key' not found.")
            raise

    def create_widgets(self):
        # Frames for grouping
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

        # Determine the width based on the longest label
        max_label_length = max(len(label) for label, _ in self.fields)
        field_width = max_label_length + 5  # Add padding for the longest string

        # Create patient information fields
        for i, (label, value) in enumerate(self.fields):
            if label in ["First Name:", "Last Name:", "Date of Birth:", "Age:"]:
                parent_frame = patient_frame
                row_index = i  # Row index in patient_frame
            else:
                parent_frame = medical_frame
                row_index = i - 4  # Adjust row index for medical_frame

            ttk.Label(parent_frame, text=label).grid(row=row_index, column=0, sticky="w", pady=5)
            if isinstance(value, list):  # Dropdown (Combobox)
                widget = ttk.Combobox(
                    parent_frame,
                    values=value,
                    width=field_width,
                    state="readonly"
                )
            elif value == "date":  # Use DateEntry for date fields
                widget = DateEntry(
                    parent_frame,
                    width=field_width - 2,
                    background='darkblue',
                    foreground='white',
                    borderwidth=2,
                    date_pattern='y-mm-dd'  # Set date format
                )
            else:  # Entry widget
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

    def submit_info(self):
        # Check if all fields are filled
        for label, widget in self.widgets.items():
            if isinstance(widget, ttk.Combobox) and not widget.get():
                mb.showerror("Error", f"Please fill in the {label.lower()}")
                return
            elif isinstance(widget, (ttk.Entry, DateEntry)) and not widget.get().strip():
                mb.showerror("Error", f"Please fill in the {label.lower()}")
                return

        # Process the collected data
        data = {label: widget.get() for label, widget in self.widgets.items()}
        print("Collected Data:", data)  # Debugging purposes

        # Preprocess the data to match the model's expected input
        try:
            input_data = self.preprocess_data(data)
            prediction = self.model.predict(input_data)
            result = prediction[0]

            # Store the prediction result
            self.prediction_result = result

            # Display the prediction result
            if result == 0:
                mb.showinfo("Result", "The model predicts that the patient does NOT have heart disease.")
            else:
                mb.showinfo("Result", "The model predicts that the patient HAS heart disease.")
        except Exception as e:
            mb.showerror("Error", f"An error occurred during prediction: {e}")

    def preprocess_data(self, data):
        """
        Preprocess the input data to match the model's expected format.

        :param data: Dictionary of input data from the form.
        :return: DataFrame with preprocessed data.
        """
        # Map categorical variables to numerical values
        mapping = {
            "Sex:": {"Male": 1, "Female": 0},
            "Fasting Blood Sugar > 120 mg/dL:": {"Yes": 1, "No": 0},
            "Exercise Induced Angina:": {"Yes": 1, "No": 0},
            "Chest Pain Type (0-3):": {"0": 0, "1": 1, "2": 2, "3": 3},
            "Resting ECG:": {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2},
            "Slope of Peak Exercise ST Segment:": {"Upsloping": 0, "Flat": 1, "Downsloping": 2},
            "Number of Major Vessels:": {"0": 0, "1": 1, "2": 2, "3": 3},
            "Thalassemia:": {"Normal": 3, "Fixed Defect": 6, "Reversible Defect": 7},
        }

        # Map form labels to model feature names
        label_to_feature = {
            "Age:": "age",
            "Sex:": "sex",
            "Chest Pain Type (0-3):": "cp",
            "Resting Blood Pressure (mmHg):": "trestbps",
            "Serum Cholesterol (mg/dL):": "chol",
            "Fasting Blood Sugar > 120 mg/dL:": "fbs",
            "Resting ECG:": "restecg",
            "Max Heart Rate (BPM):": "thalach",
            "Exercise Induced Angina:": "exang",
            "ST Depression:": "oldpeak",
            "Slope of Peak Exercise ST Segment:": "slope",
            "Number of Major Vessels:": "ca",
            "Thalassemia:": "thal"
        }

        # List of feature names in the correct order
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
                    value = mapping[label].get(value)
                    if value is None:
                        raise ValueError(f"Invalid value for {label}")
                else:
                    # Convert to numeric
                    try:
                        value = float(value)
                    except ValueError:
                        raise ValueError(f"Invalid input for {label}: must be a number.")
                processed_data.append(value)
            else:
                raise ValueError(f"Missing value for {label}")

        # Create a DataFrame with correct feature names
        input_df = pd.DataFrame([processed_data], columns=feature_order)
        return input_df

    def save_report(self):
        """Save the data and prediction result into 'hdisrep.json' with encryption."""
        if self.prediction_result is None:
            mb.showwarning("Warning", "Please submit the form to get a prediction before saving the report.")
            return

        # Collect data
        data = {label.strip(':'): widget.get() for label, widget in self.widgets.items()}

        # Add prediction result
        if self.prediction_result == 0:
            result_text = "The patient does NOT have heart disease."
        else:
            result_text = "The patient HAS heart disease."

        data["Prediction Result"] = result_text

        # Create the key using First Name, Last Name, and Date of Birth
        first_name = data.get("First Name", "").strip()
        last_name = data.get("Last Name", "").strip()
        date_of_birth = data.get("Date of Birth", "").strip()

        if not first_name or not last_name or not date_of_birth:
            mb.showerror("Error", "First Name, Last Name, and Date of Birth are required to save the report.")
            return

        key = f"{first_name}_{last_name}_{date_of_birth}"

        # Load existing data if the file exists, decrypting it first
        reports = {}
        if os.path.exists("hdisrep.json"):
            try:
                with open("hdisrep.json", "rb") as f:
                    encrypted_data = f.read()
                    if encrypted_data:
                        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                        reports = json.loads(decrypted_data.decode('utf-8'))
                    else:
                        # File is empty
                        reports = {}
            except Exception as e:
                # Handle decryption error
                response = mb.askyesno("Error", f"An error occurred while decrypting 'hdisrep.json': {e}\n\n"
                                                "Do you want to overwrite the file with new data?")
                if response:
                    # Overwrite the file
                    reports = {}
                else:
                    # Do not overwrite, exit the method
                    return
        else:
            # File does not exist; initialize empty reports dictionary
            reports = {}

        # Add or update the patient's data
        reports[key] = data

        # Save and encrypt the updated data
        try:
            json_data = json.dumps(reports, indent=4)
            encrypted_data = self.cipher_suite.encrypt(json_data.encode('utf-8'))
            with open("hdisrep.json", "wb") as f:
                f.write(encrypted_data)
            mb.showinfo("Success", f"Report saved and encrypted successfully under key '{key}' in 'hdisrep.json'.")
        except Exception as e:
            mb.showerror("Error", f"An error occurred while saving and encrypting the report: {e}")
