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
    def setup_ui(self):
    # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Python Script Performance Comparator",
                            font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Code input section
        self.create_code_input_section(main_frame)

        # Run button
        self.run_button = ttk.Button(main_frame, text="Run Comparison",
                                    command=self.run_comparison, style="Accent.TButton")
        self.run_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Results section
        self.create_results_section(main_frame)

    def create_code_input_section(self, parent):
    # Script 1 input
        script1_frame = ttk.LabelFrame(parent, text="Script 1", padding="10")
        script1_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        script1_frame.columnconfigure(0, weight=1)
        script1_frame.rowconfigure(1, weight=1)

        # Script 1 buttons frame
        script1_buttons_frame = ttk.Frame(script1_frame)
        script1_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        script1_buttons_frame.columnconfigure(0, weight=1)
        script1_buttons_frame.columnconfigure(1, weight=1)
        script1_buttons_frame.columnconfigure(2, weight=1)

        # Script 1 buttons
        self.copy1_button = ttk.Button(script1_buttons_frame, text="Copy",
                                    command=lambda: self.copy_text(self.script1_text))
        self.copy1_button.grid(row=0, column=0, padx=(0, 2))

        self.paste1_button = ttk.Button(script1_buttons_frame, text="Paste",
                                    command=lambda: self.paste_text(self.script1_text))
        self.paste1_button.grid(row=0, column=1, padx=2)

        self.clean1_button = ttk.Button(script1_buttons_frame, text="Clean",
                                    command=lambda: self.clean_text(self.script1_text))
        self.clean1_button.grid(row=0, column=2, padx=(2, 0))

        self.script1_text = scrolledtext.ScrolledText(script1_frame, width=50, height=15,
                                                    font=("Consolas", 10))
        self.script1_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Default script 1
        default_script1 = '''# Example script 1
        import time
import math

# Different approach - mathematical operations
result = 0
for i in range(500000):
    result += math.sin(i) * math.cos(i)

# Create different variables
my_tuple = (1, 2, 3, 4, 5)
my_set = {1, 2, 3, 4, 5}
my_float = 3.14159

print(f"Result: {result}")
print(f"Tuple: {my_tuple}")
print(f"Set: {my_set}")'''


def main():
    root = tk.Tk()
    app = ScriptComparator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
