# main.py
import tkinter as tk
from tkinter import ttk
from tabs.PatientFormTab import PatientFormTab
from tabs.GetPatientInfoTab import GetPatientInfoTab
from tabs.ViewGraphTab import ViewGraphTab
from model.Model import Model

class HeartDiseaseAnalyzerApp:
    def __init__(self, root, model):
        self.root = root
        self.model = model  # Store the model instance
        self.root.title("Heart Disease Analyzer")
        self.root.geometry("768x1024")
        self.root.resizable(False, False)
        self.center_window()

        # Header title
        tk.Label(
            root,
            text="Heart Disease Analyzer",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=10,
        ).pack(fill="x")

        # Add Notebook (Tabs)
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=10)

        # Add tabs
        self.add_tabs()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_x = (screen_width // 2) - (768 // 2)
        window_y = (screen_height // 2) - (1024 // 2)
        self.root.geometry(f"+{window_x}+{window_y}")

    def add_tabs(self):
        # Initialize and add tabs
        patient_form_tab = PatientFormTab(self.tab_control, self.model)
        self.tab_control.add(patient_form_tab.frame, text="Patient Form")

        get_patient_info_tab = GetPatientInfoTab(self.tab_control)
        self.tab_control.add(get_patient_info_tab.frame, text="Get Patient Info")

        view_graph_tab = ViewGraphTab(self.tab_control)
        self.tab_control.add(view_graph_tab.frame, text="View Graph")

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()  # Instantiate and train the model
    app = HeartDiseaseAnalyzerApp(root, model)
    root.mainloop()
