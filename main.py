import json
import os


def format_code(code):
    # Escape double quotes and preserve newlines
    return code.replace("\\\\", "\\").replace("\\n", "\n")


def append_to_json_file(test_code, entity_code, framework_name, file_path):
    print('start append_to_json_file')
    # Format the codes
    formatted_test_code = format_code(test_code)
    formatted_entity_code = format_code(entity_code)

    # Create the JSON object
    json_object = {
        "prompt": "Write a unit test using {} framework for this code".format(framework_name),
        "framework": framework_name,
        "code": formatted_entity_code,
        "result": formatted_test_code
    }

    # Read the existing data from the file if it exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new JSON object to the data
    data.append(json_object)

    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main(test_file_path, output_file_path):
    # Read inputs from the file
    with open(test_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        parts = content.split("/////")
        if len(parts) >= 3:
            test_code = parts[0].strip()
            entity_code = parts[1].strip()
            framework_name = parts[2].strip()
        else:
            raise ValueError("Input file is not in the correct format")

    # Append the JSON object to the file
    append_to_json_file(test_code, entity_code, framework_name, output_file_path)


if __name__ == "__main__":
    test_file_path = "C:\\Users\\1\\OneDrive\\Рабочий стол\\python\\pytest\\input.txt"
    output_file_path = "C:\\Users\\1\\OneDrive\\Рабочий стол\\python\\pytest\\pytest_jsons.txt"
    main(test_file_path, output_file_path)
