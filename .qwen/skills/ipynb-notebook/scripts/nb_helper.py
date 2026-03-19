#!/usr/bin/env python3
"""
Утилиты для быстрого редактирования Jupyter notebooks.

Использование:
    python nb_helper.py <notebook.ipynb> <command> [args]

Команды:
    list              - Показать все ячейки с ID
    get <id>          - Показать содержимое ячейки
    delete <id>       - Удалить ячейку по ID
    insert <pos>      - Вставить новую ячейку после позиции
    run               - Запустить ноутбук с papermill
"""

import json
import sys
from pathlib import Path


def load_notebook(path: str) -> dict:
    """Загрузить ноутбук из файла."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_notebook(nb: dict, path: str) -> None:
    """Сохранить ноутбук в файл."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)


def list_cells(nb: dict) -> None:
    """Вывести список всех ячеек с ID."""
    for i, cell in enumerate(nb['cells']):
        cell_id = cell.get('metadata', {}).get('id', '<no id>')
        cell_type = cell['cell_type']
        source = ''.join(cell['source'][:50])  # Первые 50 символов
        source = source.replace('\n', ' ')
        print(f"[{i}] ID: {cell_id:20} | Type: {cell_type:8} | {source}...")


def get_cell(nb: dict, cell_id: str) -> None:
    """Найти и вывести ячейку по ID."""
    for cell in nb['cells']:
        if cell.get('metadata', {}).get('id') == cell_id:
            print(f"Type: {cell['cell_type']}")
            print(f"Source:\n{''.join(cell['source'])}")
            return
    print(f"Ячейка с ID '{cell_id}' не найдена")


def delete_cell(nb: dict, cell_id: str) -> bool:
    """Удалить ячейку по ID."""
    original_len = len(nb['cells'])
    nb['cells'] = [c for c in nb['cells'] if c.get('metadata', {}).get('id') != cell_id]
    return len(nb['cells']) < original_len


def create_code_cell(source: list, cell_id: str) -> dict:
    """Создать новую code ячейку."""
    return {
        "cell_type": "code",
        "source": source,
        "metadata": {"id": cell_id},
        "execution_count": None,
        "outputs": []
    }


def create_markdown_cell(source: list, cell_id: str) -> dict:
    """Создать новую markdown ячейку."""
    return {
        "cell_type": "markdown",
        "source": source,
        "metadata": {"id": cell_id}
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    nb_path = sys.argv[1]
    command = sys.argv[2]

    if not Path(nb_path).exists():
        print(f"Файл не найден: {nb_path}")
        sys.exit(1)

    nb = load_notebook(nb_path)

    if command == 'list':
        list_cells(nb)

    elif command == 'get' and len(sys.argv) > 3:
        get_cell(nb, sys.argv[3])

    elif command == 'delete' and len(sys.argv) > 3:
        if delete_cell(nb, sys.argv[3]):
            save_notebook(nb, nb_path)
            print(f"Ячейка '{sys.argv[3]}' удалена")
        else:
            print(f"Ячейка '{sys.argv[3]}' не найдена")

    else:
        print(f"Неизвестная команда: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
