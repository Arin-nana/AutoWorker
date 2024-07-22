import tkinter as tk
from tkinter import simpledialog, messagebox
import re


class ImportStack:
    def __init__(self):
        self.stack = []
        self.history = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            item = self.stack.pop()
            self.history.append(("pop", item))
            return item
        else:
            messagebox.showerror("Error", "Стек пуст!")

    def back(self):
        if self.history:
            action, item = self.history.pop()
            if action == "pop":
                self.stack.append(item)
        else:
            messagebox.showerror("Error", "История пуста!")

    def clear(self):
        self.stack.clear()
        self.history.clear()

    def get_stack(self):
        return self.stack

    def get_history(self):
        return self.history


class StackApp:
    def __init__(self, root, stack):
        self.stack = stack
        self.root = root
        self.root.title("Import Stack")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.stack_label = tk.Label(self.frame, text="Стек импортов:")
        self.stack_label.pack()

        self.stack_listbox = tk.Listbox(self.frame, height=15, width=50)
        self.stack_listbox.pack()

        self.import_entry = tk.Entry(self.frame, width=50)
        self.import_entry.pack(pady=5)

        self.add_button = tk.Button(self.frame, text="Добавить импорт", command=self.add_import)
        self.add_button.pack(pady=5)

        self.pop_button = tk.Button(self.frame, text="Pop", command=self.pop_import)
        self.pop_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Back", command=self.back_import)
        self.back_button.pack(pady=5)

        self.history_button = tk.Button(self.frame, text="Показать историю", command=self.show_history)
        self.history_button.pack(pady=5)

        self.clear_button = tk.Button(self.frame, text="Очистить стек и историю", command=self.clear_stack)
        self.clear_button.pack(pady=5)

        self.update_stack_view()

    def add_import(self):
        import_text = self.import_entry.get().strip()
        if self.validate_import(import_text):
            if "import" in import_text:
                import_parts = import_text.split("import")
                base_import = import_parts[0].strip() + " import"
                entities = import_parts[1].strip().split(',')
                for entity in entities:
                    self.stack.push(f"{base_import} {entity.strip()}")
            else:
                self.stack.push(import_text)
            self.import_entry.delete(0, tk.END)
            self.update_stack_view()
        else:
            messagebox.showerror("Error", "Неправильный формат импорта")

    def validate_import(self, import_text):
        # Проверка на наличие 'from ... import ...' или 'import ...'
        pattern = r"^(from\s+\w+(\.\w+)*\s+import\s+[\w\s,]+|import\s+\w+(\.\w+)*)$"
        return re.match(pattern, import_text)

    def pop_import(self):
        self.stack.pop()
        self.update_stack_view()

    def back_import(self):
        self.stack.back()
        self.update_stack_view()

    def clear_stack(self):
        self.stack.clear()
        self.update_stack_view()

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("История")
        history_listbox = tk.Listbox(history_window, height=15, width=50)
        history_listbox.pack(pady=10)

        for action, item in self.stack.get_history():
            history_listbox.insert(tk.END, f"{action}: {item}")

    def update_stack_view(self):
        self.stack_listbox.delete(0, tk.END)
        for item in self.stack.get_stack():
            self.stack_listbox.insert(tk.END, item)


if __name__ == "__main__":
    root = tk.Tk()
    import_stack = ImportStack()
    app = StackApp(root, import_stack)
    root.mainloop()
