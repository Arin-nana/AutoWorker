### Описание проблемы

Когда вы работаете с большими проектами, особенно при написании и тестировании кода, вам часто приходится работать с множеством импортов. В процессе работы необходимо следить за тем, какие сущности были уже проработаны, а какие еще нет. Это может быть сложно, особенно если сущностей много и они импортируются из разных модулей. В результате можно легко упустить важные детали.

### Решение

Этот скрипт помогает вам управлять импортируемыми сущностями с помощью стека. Вы можете добавлять импортируемые сущности в стек, удалять их, когда они проработаны, и, в случае ошибки, возвращать их обратно. Также вы можете просматривать историю удалений, чтобы убедиться, что все сущности были правильно обработаны. Скрипт также поддерживает проверку правильности формата импортируемых строк и возможность очистки стека и истории.

### Руководство по использованию

#### Предварительные требования

1. Убедитесь, что у вас установлен Python 3.6 или выше.
2. Установите необходимые IDE или текстовый редактор (например, VSCode) для удобства работы с кодом.

### Запуск скрипта

1. Создайте файл с приведенным ниже кодом и сохраните его, например, как `import_stack.py`.

2. Откройте командную строку (cmd) и перейдите в папку, где находится ваш скрипт:
   ```sh
   cd <путь к папке со скриптом>
   ```

3. Запустите скрипт:
   ```sh
   python import_stack.py
   ```

### Использование

1. **Добавление импортов**:
   - Введите строку импорта в формате `from module import entity1, entity2` или `import module` в поле ввода и нажмите кнопку "Добавить импорт".
   - Если формат правильный, каждый импорт добавится в стек.
   - Если формат неправильный, вы увидите сообщение об ошибке.

2. **Удаление элемента из стека**:
   - Нажмите кнопку "Pop" для удаления верхнего элемента из стека. Этот элемент будет добавлен в историю.

3. **Возврат элемента в стек**:
   - Нажмите кнопку "Back" для возврата последнего удаленного элемента из истории в стек.

4. **Очистка стека и истории**:
   - Нажмите кнопку "Очистить стек и историю" для удаления всех элементов из стека и очистки истории действий.

5. **Просмотр истории**:
   - Нажмите кнопку "Показать историю" для открытия окна с историей действий.

### Подробные комментарии к коду

```python
import tkinter as tk
from tkinter import simpledialog, messagebox
import re


class ImportStack:
    def __init__(self):
        """Инициализация стека и истории действий"""
        self.stack = []
        self.history = []

    def push(self, item):
        """Добавляет элемент в стек"""
        self.stack.append(item)

    def pop(self):
        """Удаляет верхний элемент из стека и добавляет его в историю"""
        if self.stack:
            item = self.stack.pop()
            self.history.append(("pop", item))
            return item
        else:
            messagebox.showerror("Error", "Стек пуст!")

    def back(self):
        """Возвращает последний удаленный элемент обратно в стек"""
        if self.history:
            action, item = self.history.pop()
            if action == "pop":
                self.stack.append(item)
        else:
            messagebox.showerror("Error", "История пуста!")

    def clear(self):
        """Очищает стек и историю"""
        self.stack.clear()
        self.history.clear()

    def get_stack(self):
        """Возвращает текущий стек"""
        return self.stack

    def get_history(self):
        """Возвращает историю действий"""
        return self.history


class StackApp:
    def __init__(self, root, stack):
        """Инициализирует GUI и компоненты"""
        self.stack = stack
        self.root = root
        self.root.title("Import Stack")

        # Создание фрейма для размещения компонентов
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Метка для стека импортов
        self.stack_label = tk.Label(self.frame, text="Стек импортов:")
        self.stack_label.pack()

        # Listbox для отображения стека
        self.stack_listbox = tk.Listbox(self.frame, height=15, width=50)
        self.stack_listbox.pack()

        # Поле ввода для новых импортов
        self.import_entry = tk.Entry(self.frame, width=50)
        self.import_entry.pack(pady=5)

        # Кнопка для добавления импорта
        self.add_button = tk.Button(self.frame, text="Добавить импорт", command=self.add_import)
        self.add_button.pack(pady=5)

        # Кнопка для удаления верхнего элемента из стека
        self.pop_button = tk.Button(self.frame, text="Pop", command=self.pop_import)
        self.pop_button.pack(pady=5)

        # Кнопка для возврата последнего удаленного элемента в стек
        self.back_button = tk.Button(self.frame, text="Back", command=self.back_import)
        self.back_button.pack(pady=5)

        # Кнопка для показа истории
        self.history_button = tk.Button(self.frame, text="Показать историю", command=self.show_history)
        self.history_button.pack(pady=5)

        # Кнопка для очистки стека и истории
        self.clear_button = tk.Button(self.frame, text="Очистить стек и историю", command=self.clear_stack)
        self.clear_button.pack(pady=5)

        # Обновление отображения стека
        self.update_stack_view()

    def add_import(self):
        """Добавляет импортируемые сущности в стек после проверки их формата"""
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
        """Проверяет правильность формата импортируемой строки"""
        # Проверка на наличие 'from ... import ...' или 'import ...'
        pattern = r"^(from\s+\w+(\.\w+)*\s+import\s+[\w\s,]+|import\s+\w+(\.\w+)*)$"
        return re.match(pattern, import_text)

    def pop_import(self):
        """Удаляет верхний элемент из стека"""
        self.stack.pop()
        self.update_stack_view()

    def back_import(self):
        """Возвращает последний удаленный элемент в стек"""
        self.stack.back()
        self.update_stack_view()

    def clear_stack(self):
        """Очищает стек и обновляет его отображение"""
        self.stack.clear()
        self.update_stack_view()

    def show_history(self):
        """Открывает окно с историей действий"""
        history_window = tk.Toplevel(self.root)
        history_window.title("История")
        history_listbox = tk.Listbox(history_window, height=15, width=50)
        history_listbox.pack(pady=10)

        for action, item in self.stack.get_history():
            history_listbox.insert(tk.END, f"{action}: {item}")

    def update_stack_view(self):
        """Обновляет отображение стека"""
        self.stack_listbox.delete(0, tk.END)
        for item in self.stack.get_stack():
            self.stack_listbox.insert(tk.END, item)


if __name__ == "__main__":
    root = tk.Tk()
    import_stack = ImportStack()
    app = StackApp(root, import_stack)
    root.mainloop()
```

### Подробные комментарии к коду

- **Класс `ImportStack`**:
  - `__init__(self)`: Инициализирует пустой стек и историю действий.
  - `push(self, item)`: Добавляет элемент в стек.
  - `pop(self)`: Удаляет верхний элемент из стека и добавляет его в историю.
  - `back(self)`: Возвращает последний удаленный элемент обратно в стек.
  - `clear(self)`: Очищает стек и историю.
  - `get_stack(self)`: Возвращает текущий стек.
  - `get_history(self)`: Возвращает историю действий.

- **Класс `StackApp`**:
  - `__init__(self, root, stack)`: Инициализирует GUI и компоненты.
  - `add_import(self)`: Добавляет импортируемые сущности в стек после проверки их формата.
  - `validate_import(self, import_text)`: Проверяет правильность формата импортируемой строки.
  - `pop_import(self)`: Удаляет верхний элемент из стека.
  - `back_import(self)`: Возвращает последний удаленный элемент в стек.
  - `clear_stack(self)`: Очищает стек и обновляет его отображение.
  - `show

_history(self)`: Открывает окно с историей действий.
  - `update_stack_view(self)`: Обновляет отображение стека.

### Подробное руководство по использованию

#### 1. Инициализация стека и истории
Класс `ImportStack` используется для управления стеком импортируемых сущностей и историей действий с ними. Он поддерживает следующие методы:
- `push(item)`: добавляет элемент в стек.
- `pop()`: удаляет верхний элемент из стека и сохраняет его в историю.
- `back()`: возвращает последний удаленный элемент из истории в стек.
- `clear()`: очищает стек и историю.
- `get_stack()`: возвращает текущий стек.
- `get_history()`: возвращает историю действий.

#### 2. Создание графического интерфейса
Класс `StackApp` отвечает за создание графического интерфейса с помощью Tkinter. Он предоставляет функциональность для добавления, удаления, возврата элементов и просмотра истории. Также включает кнопки для выполнения этих операций.

#### 3. Запуск скрипта
1. Сохраните приведенный выше код в файл, например `import_stack.py`.
2. Откройте командную строку и перейдите в папку, где находится ваш скрипт:
   ```sh
   cd <путь к папке со скриптом>
   ```
3. Запустите скрипт:
   ```sh
   python import_stack.py
   ```

#### 4. Использование интерфейса

**Добавление импортов**
1. Введите строку импорта в формате `from module import entity1, entity2` или `import module` в поле ввода.
2. Нажмите кнопку "Добавить импорт".
3. Если формат правильный, каждый импорт добавится в стек как отдельная строка.
4. Если формат неправильный, вы увидите сообщение об ошибке.

**Удаление элемента из стека**
1. Нажмите кнопку "Pop" для удаления верхнего элемента из стека.
2. Этот элемент будет добавлен в историю.

**Возврат элемента в стек**
1. Нажмите кнопку "Back" для возврата последнего удаленного элемента из истории в стек.

**Очистка стека и истории**
1. Нажмите кнопку "Очистить стек и историю" для удаления всех элементов из стека и очистки истории действий.

**Просмотр истории**
1. Нажмите кнопку "Показать историю" для открытия окна с историей действий.

#### Пример использования

1. Введите в поле ввода строку: `from tkinter import simpledialog, messagebox`.
2. Нажмите "Добавить импорт". В стек добавятся два элемента: `from tkinter import simpledialog` и `from tkinter import messagebox`.
3. Нажмите "Pop" для удаления верхнего элемента из стека.
4. Нажмите "Back" для возврата удаленного элемента в стек.
5. Нажмите "Очистить стек и историю" для очистки всех элементов и истории.
6. Нажмите "Показать историю" для просмотра всех действий.

Таким образом, этот скрипт позволяет удобно управлять импортируемыми сущностями, обеспечивая их добавление, удаление, возврат и просмотр истории действий.