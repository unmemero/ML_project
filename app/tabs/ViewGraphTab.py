import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess

"""
- Shows image of graph traversal in image shower
"""
class ViewGraphTab:

    # Constructor
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    # Widget maker for button
    def create_widgets(self):
        """Create widgets for the tab."""
        ttk.Label(
            self.frame,
            text="Graph",
            font=("Arial", 14),
            padding=10
        ).pack()

        # aDD BUTTON STYLE
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
        """Open the SVG image using the default image viewer."""
        svg_path = "images/tree.svg"
        absolute_path = os.path.abspath(svg_path)

        if not os.path.exists(absolute_path):
            tk.messagebox.showerror("Error", f"The file '{svg_path}' does not exist.")
            return

        try:
            if sys.platform.startswith('darwin'):
                # macOS
                subprocess.call(('open', absolute_path))
            elif os.name == 'nt':
                # Windows
                os.startfile(absolute_path)
            elif os.name == 'posix':
                # Linux and other Unix-like systems
                subprocess.call(('xdg-open', absolute_path))
            else:
                tk.messagebox.showerror("Error", "Unsupported operating system.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not open the image: {e}")
