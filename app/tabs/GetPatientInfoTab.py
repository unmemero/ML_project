import tkinter as tk
from tkinter import ttk, messagebox as mb

class GetPatientInfoTab:
    """Encapsulates the Get Patient Info functionality."""

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Get patient information.", font=("Arial", 14)).pack(pady=10)
        tk.Button(
            self.frame,
            text="Get Info",
            command=self.get_patient_info,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
        ).pack(pady=20)

    def get_patient_info(self):
        mb.showinfo("Get Patient Info", "Fetching patient information...")