import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import tracemalloc
import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
import ast
import inspect
from types import ModuleType
import gc

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
import random

# Simulate some work
result = 0
for i in range(1000000):
    result += random.random()

# Create some variables to track
my_list = [i for i in range(1000)]
my_dict = {"key": "value", "number": 42}
my_string = "Hello, World!"

print(f"Result: {result}")
print(f"List length: {len(my_list)}")
print(f"Dictionary: {my_dict}")'''

        self.script1_text.insert(tk.END, default_script1)

        # Script 2 input
        script2_frame = ttk.LabelFrame(parent, text="Script 2", padding="10")
        script2_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        script2_frame.columnconfigure(0, weight=1)
        script2_frame.rowconfigure(1, weight=1)

        # Script 2 buttons frame
        script2_buttons_frame = ttk.Frame(script2_frame)
        script2_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        script2_buttons_frame.columnconfigure(0, weight=1)
        script2_buttons_frame.columnconfigure(1, weight=1)
        script2_buttons_frame.columnconfigure(2, weight=1)

        # Script 2 buttons
        self.copy2_button = ttk.Button(script2_buttons_frame, text="Copy",
                                      command=lambda: self.copy_text(self.script2_text))
        self.copy2_button.grid(row=0, column=0, padx=(0, 2))

        self.paste2_button = ttk.Button(script2_buttons_frame, text="Paste",
                                       command=lambda: self.paste_text(self.script2_text))
        self.paste2_button.grid(row=0, column=1, padx=2)

        self.clean2_button = ttk.Button(script2_buttons_frame, text="Clean",
                                       command=lambda: self.clean_text(self.script2_text))
        self.clean2_button.grid(row=0, column=2, padx=(2, 0))

        self.script2_text = scrolledtext.ScrolledText(script2_frame, width=50, height=15,
                                                     font=("Consolas", 10))
        self.script2_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Default script 2
        default_script2 = '''# Example script 2
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

        self.script2_text.insert(tk.END, default_script2)

    def copy_text(self, text_widget):
        """Copy all text from the specified text widget to clipboard."""
        try:
            text_content = text_widget.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(text_content)
            messagebox.showinfo("Copy", "Text copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy text: {str(e)}")

    def paste_text(self, text_widget):
        """Paste text from clipboard to the specified text widget."""
        try:
            clipboard_content = self.root.clipboard_get()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, clipboard_content)
            messagebox.showinfo("Paste", "Text pasted from clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste text: {str(e)}")

    def clean_text(self, text_widget):
        """Clear all text from the specified text widget."""
        try:
            text_widget.delete(1.0, tk.END)
            messagebox.showinfo("Clean", "Text area cleared!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear text: {str(e)}")

    def create_results_section(self, parent):
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Performance Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        results_frame.rowconfigure(0, weight=1)

        # Script 1 results
        self.result1_frame = ttk.LabelFrame(results_frame, text="Script 1 Results", padding="10")
        self.result1_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.result1_frame.columnconfigure(0, weight=1)
        self.result1_frame.rowconfigure(0, weight=1)

        self.result1_text = scrolledtext.ScrolledText(self.result1_frame, width=50, height=15,
                                                     font=("Consolas", 9), state=tk.DISABLED)
        self.result1_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Script 2 results
        self.result2_frame = ttk.LabelFrame(results_frame, text="Script 2 Results", padding="10")
        self.result2_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        self.result2_frame.columnconfigure(0, weight=1)
        self.result2_frame.rowconfigure(0, weight=1)

        self.result2_text = scrolledtext.ScrolledText(self.result2_frame, width=50, height=15,
                                                     font=("Consolas", 9), state=tk.DISABLED)
        self.result2_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def run_comparison(self):
        # Disable run button during execution
        self.run_button.config(state=tk.DISABLED)
        self.run_button.config(text="Running...")

        # Clear previous results
        self.clear_results()

        # Get scripts
        script1 = self.script1_text.get(1.0, tk.END)
        script2 = self.script2_text.get(1.0, tk.END)

        # Run scripts in separate threads
        thread1 = threading.Thread(target=self.execute_script, args=(script1, 1))
        thread2 = threading.Thread(target=self.execute_script, args=(script2, 2))

        thread1.start()
        thread2.start()

        # Monitor threads
        self.monitor_threads(thread1, thread2)

    def monitor_threads(self, thread1, thread2):
        if thread1.is_alive() or thread2.is_alive():
            self.root.after(100, lambda: self.monitor_threads(thread1, thread2))
        else:
            # Re-enable run button
            self.run_button.config(state=tk.NORMAL)
            self.run_button.config(text="Run Comparison")

    def clear_results(self):
        self.result1_text.config(state=tk.NORMAL)
        self.result1_text.delete(1.0, tk.END)
        self.result1_text.config(state=tk.DISABLED)

        self.result2_text.config(state=tk.NORMAL)
        self.result2_text.delete(1.0, tk.END)
        self.result2_text.config(state=tk.DISABLED)

    def execute_script(self, script_code, script_num):
        try:
            # Start memory tracking
            tracemalloc.start()

            # Capture stdout and stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()

            # Create a new namespace for execution
            namespace = {}

            # Measure execution time
            start_time = time.time()

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(script_code, namespace)

            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

            # Get memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Get variables (excluding built-ins and special names)
            variables = self.extract_variables(namespace)

            # Get output
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()

            # Format results
            result_text = self.format_results(execution_time, current, peak,
                                            variables, stdout_output, stderr_output)

            # Update UI in main thread
            self.root.after(0, lambda: self.update_result_display(script_num, result_text))

        except Exception as e:
            error_text = f"Error executing script {script_num}:\n\n"
            error_text += f"Exception: {type(e).__name__}\n"
            error_text += f"Message: {str(e)}\n\n"
            error_text += "Traceback:\n"
            error_text += traceback.format_exc()

            self.root.after(0, lambda: self.update_result_display(script_num, error_text))

    def extract_variables(self, namespace):
        """Extract user-defined variables from namespace, excluding built-ins and special names."""
        variables = {}
        builtins = set(dir(__builtins__)) if hasattr(__builtins__, '__dir__') else set()

        for name, value in namespace.items():
            # Skip built-ins, special names, and modules
            if (name.startswith('_') or
                name in builtins or
                name in ['__builtins__', '__name__', '__doc__', '__package__'] or
                isinstance(value, ModuleType)):
                continue

            # Limit the display of large objects
            if isinstance(value, (list, tuple)) and len(value) > 20:
                variables[name] = f"{type(value).__name__} with {len(value)} items: {str(value[:10])}..."
            elif isinstance(value, (dict, set)) and len(value) > 10:
                variables[name] = f"{type(value).__name__} with {len(value)} items: {str(list(value)[:5])}..."
            else:
                variables[name] = value

        return variables

    def format_results(self, execution_time, current_memory, peak_memory,
                      variables, stdout_output, stderr_output):
        """Format the results for display."""
        result = f"PERFORMANCE METRICS\n"
        result += f"{'='*50}\n"
        result += f"Execution Time: {execution_time:.2f} ms\n"
        result += f"Current Memory: {current_memory / 1024:.2f} KB\n"
        result += f"Peak Memory: {peak_memory / 1024:.2f} KB\n\n"

        result += f"VARIABLES\n"
        result += f"{'='*50}\n"
        if variables:
            for name, value in variables.items():
                result += f"{name}: {value}\n"
        else:
            result += "No user-defined variables found.\n"
        result += "\n"

        if stdout_output:
            result += f"STDOUT\n"
            result += f"{'='*50}\n"
            result += stdout_output + "\n"

        if stderr_output:
            result += f"STDERR\n"
            result += f"{'='*50}\n"
            result += stderr_output + "\n"

        return result

    def update_result_display(self, script_num, result_text):
        """Update the result display for the specified script."""
        if script_num == 1:
            self.result1_text.config(state=tk.NORMAL)
            self.result1_text.delete(1.0, tk.END)
            self.result1_text.insert(tk.END, result_text)
            self.result1_text.config(state=tk.DISABLED)
        else:
            self.result2_text.config(state=tk.NORMAL)
            self.result2_text.delete(1.0, tk.END)
            self.result2_text.insert(tk.END, result_text)
            self.result2_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ScriptComparator(root)
    root.mainloop()

if __name__ == "__main__":
    main()