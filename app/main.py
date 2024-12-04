# main.py
import tkinter as tk
from tkinter import ttk
from tabs.PatientFormTab import PatientFormTab
from tabs.GetPatientInfoTab import GetPatientInfoTab
from tabs.ViewGraphTab import ViewGraphTab
from model.Model import Model

"""
- Main GUI application integrating all the tabs and the model.
- The model is instantiated and trained here.
"""


class HeartDiseaseAnalyzerApp:

    # Main App Constructor
    def __init__(self, root, model):
        self.root = root
        self.model = model 
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

        # Add Tabs
        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=10)
        self.add_tabs()

    # Center window on screen
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_x = (screen_width // 2) - (768 // 2)
        window_y = (screen_height // 2) - (1024 // 2)
        self.root.geometry(f"+{window_x}+{window_y}")

    # Init the tabs
    def add_tabs(self):
        patient_form_tab = PatientFormTab(self.tab_control, self.model)
        self.tab_control.add(patient_form_tab.frame, text="Patient Form")

        get_patient_info_tab = GetPatientInfoTab(self.tab_control)
        self.tab_control.add(get_patient_info_tab.frame, text="Get Patient Info")

        view_graph_tab = ViewGraphTab(self.tab_control)
        self.tab_control.add(view_graph_tab.frame, text="View Graph")

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    app = HeartDiseaseAnalyzerApp(root, model)
    root.mainloop()
