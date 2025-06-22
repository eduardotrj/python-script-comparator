import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time

class ScriptComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Script Performance Comparator")
        self.root.geometry("1400x900")

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        self.setup_ui()