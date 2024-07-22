import os
import unittest
from typing import List, Set
from process_test import read_file, write_to_file, search_keywords, extract_entities, remove_duplicate_entities, \
    process_test_file


class TestProcessTestFile(unittest.TestCase):

    def setUp(self):
        # Создание временной рабочей директории
        self.test_dir = 'test_dir'
        os.makedirs(self.test_dir, exist_ok=True)

        # Создание тестового файла
        self.test_file_path = os.path.join(self.test_dir, 'test_file.py')
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write('from code_directory import MyClass, my_function, my_variable\n\n'
                    'def test_something():\n'
                    '    obj = MyClass()\n'
                    '    result = my_function()\n'
                    '    assert result == obj.expected_result()\n'
                    '    assert my_variable == \'test\'\n')

        # Создание файлов сущностей
        self.code_directory = os.path.join(self.test_dir, 'code_directory')
        os.makedirs(self.code_directory, exist_ok=True)
        self.create_entity_file('MyClass.txt',
                                'class MyClass:\n    def __init__(self):\n        self.data = \'expected_result\'\n\n    def expected_result(self):\n        return self.data\n')
        self.create_entity_file('my_function.txt', 'def my_function():\n    return \'expected_result\'\n')
        self.create_entity_file('my_variable.txt', 'my_variable = \'test\'\n')

        # Создание выходного файла
        self.output_file_path = os.path.join(self.test_dir, 'output_file.txt')

    def tearDown(self):
        # Удаление тестовой директории после тестов
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def create_entity_file(self, file_name, content):
        # Создаёт файлы сущностей в указанной директории с переданным содержимым
        file_path = os.path.join(self.code_directory, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def test_read_file(self):
        # Проверяет чтение содержимого файла
        content = read_file(self.test_file_path)
        self.assertIn('from code_directory import MyClass, my_function, my_variable', content)

    def test_write_to_file(self):
        # Проверяет запись содержимого в файл
        test_content = 'This is a test.'
        write_to_file(self.output_file_path, test_content)
        with open(self.output_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn(test_content, content)

    def test_search_keywords(self):
        # Проверяет поиск ключевых слов в коде теста
        test_code = 'from code_directory import MyClass, my_function, my_variable\n'
        keywords = ['MyClass', 'my_function', 'my_variable']
        found_keywords = search_keywords(test_code, keywords)
        self.assertListEqual(found_keywords, ['MyClass', 'my_function', 'my_variable'])

    def test_extract_entities(self):
        # Проверяет извлечение названий методов и классов из текста
        test_code = ('class MyClass:\n'
                     '    def __init__(self):\n'
                     '        self.data = \'expected_result\'\n\n'
                     '    def expected_result(self):\n'
                     '        return self.data\n'
                     'def my_function():\n'
                     '    return \'expected_result\'\n')
        entities = extract_entities(test_code)
        self.assertSetEqual(entities, {'MyClass', 'expected_result', 'my_function'})

    def test_extract_entities_exclude_init(self):
        # Проверяет извлечение названий методов и классов из текста, исключая метод __init__
        test_code = ('class MyClass:\n'
                     '    def __init__(self):\n'
                     '        self.data = \'expected_result\'\n\n'
                     '    def expected_result(self):\n'
                     '        return self.data\n'
                     'def my_function():\n'
                     '    return \'expected_result\'\n')
        entities = extract_entities(test_code)
        self.assertSetEqual(entities, {'MyClass', 'expected_result', 'my_function'})
        self.assertNotIn('__init__', entities)

    def test_remove_duplicate_entities(self):
        # Проверяет удаление дублирующихся реализаций методов и классов из файла
        duplicate_code = ('class MyClass:\n'
                          '    def __init__(self):\n'
                          '        self.data = \'expected_result\'\n\n'
                          '    def expected_result(self):\n'
                          '        return self.data\n'
                          'class MyClass:\n'
                          '    def __init__(self):\n'
                          '        self.data = \'expected_result\'\n\n'
                          '    def expected_result(self):\n'
                          '        return self.data\n'
                          'def my_function():\n'
                          '    return \'expected_result\'\n'
                          'def my_function():\n'
                          '    return \'expected_result\'\n')
        write_to_file(self.output_file_path, duplicate_code)
        remove_duplicate_entities(self.output_file_path)
        content = read_file(self.output_file_path)
        self.assertNotIn(
            'class MyClass:\n    def __init__(self):\n        self.data = \'expected_result\'\n\n    def expected_result(self):\n        return self.data\n\nclass MyClass:',
            content)
        self.assertNotIn('def my_function():\n    return \'expected_result\'\n\ndef my_function():', content)

    def test_process_test_file(self):
        # Проверяет полный процесс обработки тестового файла, включая добавление кода сущностей и удаление дублирующихся реализаций
        keywords = ['MyClass', 'my_function', 'my_variable']
        process_test_file(self.test_file_path, keywords, self.code_directory, self.output_file_path)
        content = read_file(self.output_file_path)
        self.assertIn('class MyClass', content)
        self.assertIn('def my_function', content)
        self.assertIn('my_variable = \'test\'', content)


if __name__ == '__main__':
    unittest.main()
