### Инструкция по использованию скрипта для генерации JSON объектов

Этот скрипт предназначен для чтения кода теста и тестируемой сущности из входного файла, форматирования этих данных и сохранения их в JSON файл. Следуйте инструкциям ниже для правильного использования скрипта.

#### Предварительные требования

1. Убедитесь, что у вас установлен Python 3.6 или выше.
2. Установите необходимые IDE или текстовый редактор (например, VSCode) для удобства работы с кодом.

#### Структура файлов и папок

1. Создайте основную папку для работы, например `work`:
   ```
   <основная папка>
   ```

2. Внутри основной папки создайте подкаталоги для каждого языка программирования и фреймворка. Пример для Python:
   ```
   <основная папка>/<язык программирования>/<фреймворк>
   ```

3. Создайте файл `input.txt` в папке с фреймворком с содержимым в следующем формате:
   ```
   <код теста>
   /////
   <код тестируемой сущности>
   /////
   <название фреймворка>
   ```

#### Пример содержимого `input.txt`

```txt
def test_create_item(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content
/////
@router.post("/", response_model=ItemPublic)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    item = Item.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
/////
pytest
```

#### Запуск скрипта

1. Поместите файл `input.txt` в нужную папку с фреймворком.

2. Создайте и сохраните следующий скрипт Python:

```python
import json
import os

def format_code(code):
    # Экранирование двойных кавычек и сохранение переносов строк
    return code.replace("\\\\", "\\").replace("\\n", "\n")

def append_to_json_file(test_code, entity_code, framework_name, file_path):
    # Форматирование кода
    formatted_test_code = format_code(test_code)
    formatted_entity_code = format_code(entity_code)

    # Создание JSON объекта
    json_object = {
        "prompt": "Write a unit test using {} framework for this code".format(framework_name),
        "framework": framework_name,
        "code": formatted_entity_code,
        "result": formatted_test_code
    }

    # Чтение существующих данных из файла, если он существует
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

    # Добавление нового JSON объекта к данным
    data.append(json_object)

    # Запись обновленных данных обратно в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Чтение входных данных из файла
    with open("input.txt", "r", encoding='utf-8') as file:
        content = file.read()
        parts = content.split("/////")
        if len(parts) >= 3:
            test_code = parts[0].strip()
            entity_code = parts[1].strip()
            framework_name = parts[2].strip()
            file_path = "output.txt"  # Укажите здесь путь к выходному файлу
        else:
            raise ValueError("Input file is not in the correct format")

    # Добавление JSON объекта в файл
    append_to_json_file(test_code, entity_code, framework_name, file_path)
```

3. Откройте командную строку (cmd) и перейдите в папку, где находится ваш скрипт:
   ```sh
   cd <путь к папке со скриптом>
   ```

4. Запустите скрипт:
   ```sh
   python script_name.py
   ```

#### Результат

После выполнения скрипта, файл `output.txt` будет содержать JSON объект с форматированным кодом теста и тестируемой сущности. При повторном запуске скрипта, к уже существующим объектам будет добавлен новый.

Пример содержимого `output.txt`:

```json
[
    {
        "prompt": "Write a unit test using pytest framework for this code",
        "framework": "pytest",
        "code": "@router.post(\"/\", response_model=ItemPublic)\ndef create_item(\n    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate\n) -> Any:\n    \"\"\"\n    Create new item.\n    \"\"\"\n    item = Item.model_validate(item_in, update={\"owner_id\": current_user.id})\n    session.add(item)\n    session.commit()\n    session.refresh(item)\n    return item",
        "result": "def test_create_item(\n    client: TestClient, superuser_token_headers: dict[str, str]\n) -> None:\n    data = {\"title\": \"Foo\", \"description\": \"Fighters\"}\n    response = client.post(\n        f\"{settings.API_V1_STR}/items/\",\n        headers=superuser_token_headers,\n        json=data,\n    )\n    assert response.status_code == 200\n    content = response.json()\n    assert content[\"title\"] == data[\"title\"]\n    assert content[\"description\"] == data[\"description\"]\n    assert \"id\" in content\n    assert \"owner_id\" in content"
    },
    {
        "prompt": "Write a unit test using pytest framework for this code",
        "framework": "pytest",
        "code": "def load_model_data(file_path):\n    with open(file_path, \"r\") as models_file:\n        return json.load(models_file)\n\n\ndef flatten_model_data(families):\n    for family in families:\n        for model in family[\"models\"]:\n            for file in model[\"files\"]:\n                yield model[\"repo\"], file[\"filename\"]\n\n\ndef check_model_availability(repo, filename):\n    url = hf_hub_url(repo, filename, repo_type=\"model\", revision=\"main\")\n    response = requests.head(url)\n    if response.ok:\n        return True\n    else:\n        return False",
        "result": "import json\nfrom pathlib import Path\nimport requests\nfrom huggingface_hub import hf_hub_url\nimport pytest\n\ntest_dir = Path(__file__).parent\nmodel_data = load_model_data(test_dir.parent / \"src/serge/data/models.json\")\nchecks = list(flatten_model_data(model_data))\n\n\n@pytest.mark.parametrize(\"repo,filename\", checks)\ndef test_model_available(repo, filename):\n    assert check_model_availability(repo, filename), f\"Model {repo}/{filename} not available\""
    }
]
```

Теперь у вас есть JSON файл с отформатированным кодом теста и тестируемой сущности, готовый для дальнейшего использования или анализа.