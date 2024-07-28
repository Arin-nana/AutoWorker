import os
import re

def process_test_cases(input_file_path, output_file_path, pipeline_script_path, language):
    """
    Извлекает тестовые случаи из файла, записывает их в другой файл и вызывает указанный скрипт.

    Аргументы:
    input_file_path (str): Путь к входному файлу.
    output_file_path (str): Путь к выходному файлу.
    pipeline_script_path (str): Путь к скрипту, который будет выполнен после записи тестового случая.
    language (str): Язык программирования ('python' или 'javascript').
    """
    def run_pipeline():
        """Выполняет указанный скрипт."""
        os.system(f'python {pipeline_script_path}')

    # Регулярные выражения для Python и JavaScript
    if language == 'python':
        test_case_pattern = re.compile(r'^\s*(def test|class\s)')
    elif language == 'javascript':
        test_case_pattern = re.compile(r'^\s*(it|describe|test)\s*\(')

    # Открываем входной файл для чтения
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()  # Читаем все строки файла

    in_test_case = False  # Флаг, указывающий, находимся ли мы в блоке теста
    test_case_lines = []  # Список для хранения строк текущего теста

    for line in lines:
        stripped_line = line.lstrip()  # Удаляем ведущие пробелы для проверки шаблона
        # Проверяем, начинается ли строка с шаблона для теста
        if test_case_pattern.match(stripped_line):
            if in_test_case:
                # Если мы уже в блоке теста, записываем текущий тест в файл и выполняем скрипт
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    outfile.writelines(test_case_lines)
                run_pipeline()
                test_case_lines = []  # Очищаем список строк для следующего теста
            in_test_case = True
        if in_test_case:
            test_case_lines.append(line)  # Добавляем строку в список текущего теста

    if in_test_case:
        # После обработки всех строк, если мы все еще в блоке теста, записываем и выполняем скрипт
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(test_case_lines)
        run_pipeline()

if __name__ == "__main__":
    # Путь к входному файлу, содержащему исходный код тестов
    input_file_path = r'C:\Users\Egor\Desktop\work\python\pytest\temp_test_file.txt'
    # Путь к временному выходному файлу, где будут сохраняться тесты для обработки
    output_file_path = r'C:\Users\1\OneDrive\Рабочий стол\python\pytest\input.txt'
    # Путь к скрипту, который будет выполняться после каждого теста
    pipeline_script_path = r'C:\Users\1\OneDrive\Документы\GitHub\AutoWorker\pipeline.py'
    # Язык программирования
    language = 'python'  # или 'javascript'

    # Запуск процесса обработки тестов
    process_test_cases(input_file_path, output_file_path, pipeline_script_path, language)
