import unittest
from unittest.mock import MagicMock, patch, call
import types
from script_comparator import ScriptComparator, main

# test_script_comparator.py



class TestScriptComparator(unittest.TestCase):
    def setUp(self):
        # Patch tkinter root and widgets
        self.root = MagicMock()
        self.text_widget = MagicMock()
        self.result1_text = MagicMock()
        self.result2_text = MagicMock()
        self.scrolledtext_patch = patch('tkinter.scrolledtext.ScrolledText', return_value=self.text_widget)
        self.scrolledtext_patch.start()
        self.addCleanup(self.scrolledtext_patch.stop)
        # Patch ttk.Style to avoid TclError
        self.style_patch = patch('tkinter.ttk.Style')
        self.style_patch.start()
        self.addCleanup(self.style_patch.stop)
        # Patch ttk widgets
        self.ttk_patch = patch('tkinter.ttk')
        self.ttk_patch.start()
        self.addCleanup(self.ttk_patch.stop)
        # Patch messagebox
        self.msgbox_patch = patch('tkinter.messagebox')
        self.msgbox_patch.start()
        self.addCleanup(self.msgbox_patch.stop)
        # Patch Tk
        self.tk_patch = patch('tkinter.Tk', return_value=self.root)
        self.tk_patch.start()
        self.addCleanup(self.tk_patch.stop)

    def test_init_sets_attributes(self):
        comp = ScriptComparator(self.root)
        self.assertTrue(hasattr(comp, 'root'))
        self.assertTrue(hasattr(comp, 'run_button'))

    def test_format_results_output(self):
        comp = ScriptComparator(self.root)
        result = comp.format_results(
            execution_time=123.45,
            current_memory=2048,
            peak_memory=4096,
            variables={'a': 1, 'b': 2},
            stdout_output='hello\n',
            stderr_output='error\n'
        )
        self.assertIn('PERFORMANCE METRICS', result)
        self.assertIn('Execution Time: 123.45 ms', result)
        self.assertIn('a: 1', result)
        self.assertIn('STDOUT', result)
        self.assertIn('hello', result)
        self.assertIn('STDERR', result)
        self.assertIn('error', result)

    def test_extract_variables_filters(self):
        comp = ScriptComparator(self.root)
        ns = {
            '__builtins__': {},
            '__name__': 'test',
            '_hidden': 123,
            'normal': 42,
            'mod': types.ModuleType('mod')
        }
        vars = comp.extract_variables(ns)
        self.assertIn('normal', vars)
        self.assertNotIn('_hidden', vars)
        self.assertNotIn('__builtins__', vars)
        self.assertNotIn('mod', vars)

    def test_update_result_display_script1(self):
        comp = ScriptComparator(self.root)
        comp.result1_text = self.result1_text
        comp.result2_text = self.result2_text
        comp.update_result_display(1, "abc")
        self.result1_text.config.assert_any_call(state='normal')
        self.result1_text.delete.assert_called_with(1.0, 'end')
        self.result1_text.insert.assert_called_with('end', "abc")
        self.result1_text.config.assert_any_call(state='disabled')

    def test_update_result_display_script2(self):
        comp = ScriptComparator(self.root)
        comp.result1_text = self.result1_text
        comp.result2_text = self.result2_text
        comp.update_result_display(2, "xyz")
        self.result2_text.config.assert_any_call(state='normal')
        self.result2_text.delete.assert_called_with(1.0, 'end')
        self.result2_text.insert.assert_called_with('end', "xyz")
        self.result2_text.config.assert_any_call(state='disabled')

    def test_clear_results(self):
        comp = ScriptComparator(self.root)
        comp.result1_text = self.result1_text
        comp.result2_text = self.result2_text
        comp.clear_results()
        self.result1_text.delete.assert_called_with(1.0, 'end')
        self.result2_text.delete.assert_called_with(1.0, 'end')

    def test_copy_text(self):
        comp = ScriptComparator(self.root)
        self.text_widget.get.return_value = "abc"
        comp.copy_text(self.text_widget)
        self.root.clipboard_clear.assert_called_once()
        self.root.clipboard_append.assert_called_with("abc")

    def test_paste_text(self):
        comp = ScriptComparator(self.root)
        self.root.clipboard_get.return_value = "xyz"
        comp.paste_text(self.text_widget)
        self.text_widget.delete.assert_called_with(1.0, 'end')
        self.text_widget.insert.assert_called_with('end', "xyz")

    def test_clean_text(self):
        comp = ScriptComparator(self.root)
        comp.clean_text(self.text_widget)
        self.text_widget.delete.assert_called_with(1.0, 'end')

    def test_execute_script_success(self):
        comp = ScriptComparator(self.root)
        comp.result1_text = self.result1_text
        comp.result2_text = self.result2_text
        comp.update_result_display = MagicMock()
        comp.root.after = lambda delay, func: func()
        code = "x = 1\nprint('hi')"
        comp.execute_script(code, 1)
        comp.update_result_display.assert_called()
        args = comp.update_result_display.call_args[0]
        self.assertEqual(args[0], 1)
        self.assertIn('hi', args[1])

    def test_execute_script_exception(self):
        comp = ScriptComparator(self.root)
        comp.result1_text = self.result1_text
        comp.result2_text = self.result2_text
        comp.update_result_display = MagicMock()
        comp.root.after = lambda delay, func: func()
        code = "raise ValueError('fail')"
        comp.execute_script(code, 2)
        comp.update_result_display.assert_called()
        args = comp.update_result_display.call_args[0]
        self.assertEqual(args[0], 2)
        self.assertIn('ValueError', args[1])

    def test_run_comparison_starts_threads(self):
        comp = ScriptComparator(self.root)
        comp.script1_text = MagicMock()
        comp.script2_text = MagicMock()
        comp.script1_text.get.return_value = "print(1)"
        comp.script2_text.get.return_value = "print(2)"
        comp.clear_results = MagicMock()
        comp.monitor_threads = MagicMock()
        with patch('threading.Thread') as thread_patch:
            thread1 = MagicMock()
            thread2 = MagicMock()
            thread_patch.side_effect = [thread1, thread2]
            comp.run_comparison()
            thread1.start.assert_called_once()
            thread2.start.assert_called_once()
            comp.monitor_threads.assert_called_with(thread1, thread2)
            comp.run_button.config.assert_any_call(state='disabled')
            comp.run_button.config.assert_any_call(text='Running...')

    def test_monitor_threads_reenable(self):
        comp = ScriptComparator(self.root)
        comp.run_button = MagicMock()
        t1 = MagicMock()
        t2 = MagicMock()
        t1.is_alive.return_value = False
        t2.is_alive.return_value = False
        comp.root.after = lambda delay, func: func()
        comp.monitor_threads(t1, t2)
        comp.run_button.config.assert_any_call(state='normal')
        comp.run_button.config.assert_any_call(text='Run Comparison')

    def test_main_runs(self):
        with patch('tkinter.Tk') as tk_patch:
            root = MagicMock()
            tk_patch.return_value = root
            with patch('script_comparator.ScriptComparator') as sc_patch:
                app = MagicMock()
                sc_patch.return_value = app
                with patch.object(root, 'mainloop') as ml_patch:
                    main()
                    tk_patch.assert_called_once()
                    sc_patch.assert_called_with(root)
                    ml_patch.assert_called_once()

if __name__ == "__main__":
    unittest.main()