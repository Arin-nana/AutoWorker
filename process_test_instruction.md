### Описание проблемы

Когда вы работаете с большими проектами, особенно при написании и тестировании кода, вам часто приходится работать с множеством импортов и сущностей, которые могут быть определены в разных файлах проекта. В процессе анализа тестов вам нужно быстро находить и собирать код этих сущностей. Вручную выполнять эту задачу может быть сложно и подвержено ошибкам, особенно когда сущностей много и они распределены по разным файлам. Это может привести к дублированию кода и другим ошибкам.

### Решение

Этот скрипт автоматизирует процесс поиска и добавления кода сущностей, используемых в тестах. Он парсит код теста, ищет заданные ключевые слова (имена классов, функций и т.д.) и добавляет соответствующий код из отдельных файлов в итоговый файл. Скрипт также проверяет итоговый файл на наличие дублирующихся реализаций методов и классов и удаляет их, включая соответствующие импорты и декораторы.

### Руководство по использованию

#### Предварительные требования

1. Убедитесь, что у вас установлен Python 3.6 или выше.
2. Установите необходимые IDE или текстовый редактор (например, VSCode) для удобства работы с кодом.

#### Структура файлов и папок

1. Создайте основную папку для работы, например `project`:
   ```
   project/
   ├── code_directory/
   │   ├── MyClass.txt
   │   ├── my_function.txt
   │   └── my_variable.txt
   ├── test_file.py
   └── process_test.py
   ```

2. В папке `code_directory` создайте текстовые файлы с кодом для каждой сущности, которую вы хотите обрабатывать. Например, для класса `MyClass` создайте файл `MyClass.txt`, содержащий код этого класса.

#### Пример содержимого `test_file.py`

```python
from code_directory import MyClass, my_function

def test_something():
    obj = MyClass()
    result = my_function()
    assert result == obj.expected_result()
```

#### Пример содержимого `MyClass.txt`

```python
class MyClass:
    def __init__(self):
        self.data = 'expected_result'
    
    def expected_result(self):
        return self.data
```

#### Пример содержимого `my_function.txt`

```python
def my_function():
    return 'expected_result'
```

### Скрипт `process_test.py`

```python
import os
import re
from typing import List, Set

def read_file(file_path: str) -> str:
    """Читает содержимое файла и возвращает его как строку."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_file(file_path: str, content: str) -> None:
    """Записывает содержимое в файл."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + "\n")

def search_keywords(test_code: str, keywords: List[str]) -> List[str]:
    """Ищет ключевые слова в коде теста и возвращает найденные."""
    found_keywords = []
    for keyword in keywords:
        if keyword in test_code:
            found_keywords.append(keyword)
    return found_keywords

def extract_entities(content: str) -> Set[str]:
    """Извлекает названия методов и классов из текста."""
    entities = set()
    pattern = re.compile(r'^\s*(def|class)\s+(\w+)', re.MULTILINE)
    for match in pattern.finditer(content):
        entities.add(match.group(2))
    return entities

def remove_duplicate_entities(file_path: str) -> None:
    """Удаляет дублирующиеся реализации методов и классов из файла."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Шаблон для поиска методов и классов
    entity_pattern = re.compile(r'^\s*(def|class)\s+(\w+)')
    # Шаблон для поиска импортов, декораторов и пустых строк
    import_pattern = re.compile(r'^\s*from\s+\w+|\s*import\s+|\s*@\w+')

    # Извлекаем все методы и классы из файла
    entities = extract_entities(''.join(lines))
    seen_entities = set()
    new_lines = []
    skip = False

    for i, line in enumerate(lines):
        match = entity_pattern.match(line)
        if match:
            entity_name = match.group(2)
            if entity_name in seen_entities:
                # Если сущность уже была добавлена, начинаем пропускать строки
                skip = True
            else:
                seen_entities.add(entity_name)
                skip = False

        if not skip:
            new_lines.append(line)
        elif skip and (import_pattern.match(line) or line.strip() == ''):
            # Если пропускаем строки и встречаем импорт, декоратор или пустую строку, удаляем последнюю добавленную строку
            new_lines.pop()
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def get_keywords_from_directory(code_directory: str) -> List[str]:
    """Получает список ключевых слов из имен файлов в указанной директории, удаляя расширение .txt"""
    keywords = []
    for filename in os.listdir(code_directory):
        if filename.endswith('.txt'):
            keywords.append(filename[:-4])  # удаляем расширение .txt
    return keywords

def process_test_file(test_file_path: str, code_directory: str, output_file_path: str) -> None:
    """Парсит файл теста, ищет ключевые слова и добавляет соответствующий код в выходной файл, избегая дублирования."""
    # Чтение кода теста
    test_code = read_file(test_file_path)

    # Получение ключевых слов из директории
    keywords = get_keywords_from_directory(code_directory)

    # Поиск ключевых слов в коде теста
    found_keywords = search_keywords(test_code, keywords)

    # Множество для отслеживания уже добавленных ключевых слов
    added_keywords: Set[str] = set()

    # Обработка найденных ключевых слов
    for keyword in found_keywords:
        if keyword not in added_keywords:
            keyword_file_path = os.path.join(code_directory, f"{keyword}.txt")
            if os.path.exists(keyword_file_path):
                keyword_code = read_file(keyword_file_path)
                write_to_file(output_file_path, keyword_code)
                added_keywords.add(keyword)
            else:
                print(f"Файл для ключевого слова '{keyword}' не найден по пути: {keyword_file_path}")

    # Удаление дублирующихся реализаций методов и классов
    remove_duplicate_entities(output_file_path)

# Путь к файлу теста
test_file_path: str = 'path/to/test_file.py'

# Директория, где находятся файлы с кодом для ключевых слов
code_directory: str = 'path/to/code_directory'

# Путь к выходному файлу
output_file_path: str = 'path/to/output_file.txt'

# Запуск обработки файла теста
process_test_file(test_file_path, code_directory, output_file_path)
```

### Подробные комментарии к функции `remove_duplicate_entities`

1. **Чтение файла**:
   ```python
   with open(file_path, 'r', encoding='utf-8') as file:
       lines = file.readlines()
   ```
   - Читает содержимое файла и сохраняет его в виде списка строк.

2. **Шаблоны для поиска**:
   ```python
   entity_pattern = re.compile(r'^\s*(def|class)\s+(\w+)')
   import_pattern = re.compile(r'^\s*from\s+\w+|\s*import\s+|\s*@\w+')
   ```
   - `entity_pattern`: Шаблон для поиска методов и классов.
   - `import_pattern`: Шаблон для поиска импортов, декораторов и пустых строк.

3. **Извлечение всех методов и классов из файла**:
   ```python
   entities = extract_entities(''.join(lines))
   seen_entities = set()
   new_lines = []
   skip = False
   ```
   - Извлекает все методы и классы из файла и сохраняет их в `entities`.
   - `seen_entities`: Множество для отслеживания уже добавленных сущностей.
   - `new_lines`: Список для хранения новых строк без дублирующихся реализаций.
   - `skip`: Флаг для пропуска строк, если сущность уже была добавлена.

4. **Обработка строк файла**:
   ```python
   for i, line in enumerate(lines):
       match = entity_pattern.match(line)
       if match:
           entity_name = match.group(2)
           if entity_name in seen_entities:
               skip = True
           else:
               seen_entities.add(entity_name)
               skip = False

       if not skip:
           new_lines.append(line)
       elif skip and (import_pattern.match(line) or line.strip() == ''):
           new_lines.pop()
   ```
   - Итерируется по строкам файла.
   - Если строка соответствует шаблону `entity_pattern`, проверяет, была ли эта сущность уже добавлена.
     - Если да, устанавливает

 флаг `skip` в `True`.
     - Если нет, добавляет сущность в `seen_entities` и устанавливает `skip` в `False`.
   - Если `skip` равно `False`, добавляет строку в `new_lines`.
   - Если `skip` равно `True` и строка соответствует шаблону `import_pattern` или является пустой, удаляет последнюю добавленную строку из `new_lines`.

5. **Запись обновленного содержимого в файл**:
   ```python
   with open(file_path, 'w', encoding='utf-8') as file:
       file.writelines(new_lines)
   ```
   - Записывает обновленное содержимое в файл, предварительно удалив дублирующиеся реализации методов и классов.