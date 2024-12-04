
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

"""
- Shows image of graph traversal in image viewer.
"""
class ViewGraphTab:

    # Constructor
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    # Function to get resource path
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Widget maker for button
    def create_widgets(self):
        ttk.Label(
            self.frame,
            text="Graph",
            font=("Arial", 14),
            padding=10
        ).pack()

        # Add BUTTON STYLE
        style = ttk.Style()
        style.theme_use('clam') 

        # Configure BUTTON
        style.configure('Custom.TButton',
                        background='#4CAF50',
                        foreground='white',  
                        font=('Arial', 12, 'bold'))

        # Apply STYLE
        open_button = ttk.Button(
            self.frame,
            text="Open Graph",
            command=self.open_image,
            padding=10,
            style='Custom.TButton'
        )
        open_button.pack(pady=20)

    def open_image(self):
        svg_relative_path = os.path.join("images", "tree.svg")
        svg_path = self.resource_path(svg_relative_path)

        if not os.path.exists(svg_path):
            messagebox.showerror("Error", f"The file '{svg_relative_path}' does not exist.")
            return

        try:
            if sys.platform.startswith('darwin'):
                # macOS
                subprocess.call(('open', svg_path))
            elif os.name == 'nt':
                # Windows
                os.startfile(svg_path)
            elif os.name == 'posix':
                # Linux and other Unix-like systems
                subprocess.call(('xdg-open', svg_path))
            else:
                messagebox.showerror("Error", "Unsupported operating system.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the image: {e}")
