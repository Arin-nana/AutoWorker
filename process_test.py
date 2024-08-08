import os
import re
from typing import List, Set

def read_file(file_path: str) -> str:
    """Читает содержимое файла и возвращает его как строку."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_file(file_path: str, content: str) -> None:
    """Записывает содержимое в файл."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def search_keywords(test_code: str, keywords: List[str]) -> List[str]:
    """Ищет ключевые слова в коде теста и возвращает найденные."""
    found_keywords = []
    for keyword in keywords:
        if keyword in test_code:
            found_keywords.append(keyword)
    return found_keywords

def extract_entities(content: str, language: str) -> Set[str]:
    """Извлекает названия методов и классов из текста, исключая метод __init__."""
    entities = set()
    if language == 'python':
        pattern = re.compile(r'^\s*(def|class)\s+(\w+)', re.MULTILINE)
    elif language == 'javascript':
        pattern = re.compile(r'^\s*(function|class|const|let)\s+(\w+)', re.MULTILINE)

    for match in pattern.finditer(content):
        entity_name = match.group(2)
        if entity_name != '__init__':
            entities.add(entity_name)
    return entities

def remove_duplicate_entities(content: str, language: str) -> str:
    """Удаляет дублирующиеся реализации методов и классов из строки."""
    lines = content.split('\n')
    if language == 'python':
        entity_pattern = re.compile(r'^\s*(def|class)\s+(\w+)')
    elif language == 'javascript':
        entity_pattern = re.compile(r'^\s*(function|class|const|let)\s+(\w+)')
    import_pattern = re.compile(r'^\s*from\s+\w+|\s*import\s+|\s*@\w+')

    entities = extract_entities(content, language)
    seen_entities = set()
    new_lines = []
    skip = False

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

    return '\n'.join(new_lines)

def process_test_file(test_file_path: str, keywords: List[str], code_directory: str, framework: str, language: str) -> None:
    """Парсит файл теста, ищет ключевые слова и добавляет соответствующий код в выходной файл, избегая дублирования."""
    # Чтение кода теста
    test_code = read_file(test_file_path)

    # Поиск ключевых слов в коде теста
    found_keywords = search_keywords(test_code, keywords)

    # Множество для отслеживания уже добавленных ключевых слов
    added_keywords: Set[str] = set()

    # Обработка найденных ключевых слов
    entity_code = ""
    for keyword in found_keywords:
        if keyword not in added_keywords:
            keyword_file_path = os.path.join(code_directory, f"{keyword}.txt")
            if os.path.exists(keyword_file_path):
                keyword_code = read_file(keyword_file_path)
                entity_code += keyword_code + "\n"
                added_keywords.add(keyword)
            else:
                print(f"Файл для ключевого слова '{keyword}' не найден по пути: {keyword_file_path}")

    # Удаление дублирующихся реализаций методов и классов
    entity_code = remove_duplicate_entities(entity_code.strip(), language)

    # Формирование нового содержимого файла
    new_content = f"{test_code.strip()}\n/////\n{entity_code}\n/////\n{framework}"

    # Запись нового содержимого в файл
    write_to_file(test_file_path, new_content)

# Пример использования
if __name__ == "__main__":
    # Путь к файлу теста
    test_file_path: str = r'C:\Users\1\OneDrive\Рабочий стол\python\pytest\input.txt'

    # Директория, где находятся файлы с кодом для ключевых слов
    code_directory: str = r'C:\Users\1\OneDrive\Рабочий стол\python\pytest\entities'
    keywords = [os.path.splitext(f)[0] for f in os.listdir(code_directory) if f.endswith('.txt')]

    # Фреймворк
    framework: str = 'pytest'

    # Язык программирования
    language: str = 'python'  # или 'javascript'

    # Запуск обработки файла теста
    process_test_file(test_file_path, keywords, code_directory, framework, language)
