import importlib.util
import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def import_and_run(module_path, function_name, *args):
    logging.debug(f'Импорт модуля из {module_path} и выполнение функции {function_name} с аргументами {args}')
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    func = getattr(module, function_name)
    result = func(*args)
    logging.debug(f'Результат выполнения функции {function_name}: {result}')
    return result

def main(test_file_path, keywords, code_directory, framework, output_file_path, language):
    script1_path = r'C:\Users\Egor\PycharmProjects\AutoWorker\process_test.py'
    script2_path = r'C:\Users\Egor\PycharmProjects\AutoWorker\main.py'

    logging.info('Запуск первого скрипта: process_test.py')
    import_and_run(script1_path, 'process_test_file', test_file_path, keywords, code_directory, framework, language)

    logging.info('Запуск второго скрипта: main.py')
    import_and_run(script2_path, 'main', test_file_path, output_file_path)

if __name__ == "__main__":
    test_file_path = r'C:\Users\1\OneDrive\Рабочий стол\python\pytest\input.txt'
    keywords = []
    code_directory = r'C:\Users\1\OneDrive\Рабочий стол\python\pytest\entities'
    output_file_path = r'C:\Users\1\OneDrive\Рабочий стол\python\pytest\pytest_jsons.txt'
    framework = 'pytest'
    language = 'python'  # или 'javascript'

    main(test_file_path, keywords, code_directory, framework, output_file_path, language)
