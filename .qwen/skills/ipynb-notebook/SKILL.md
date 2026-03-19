---
name: ipynb-notebook
description: Создание, редактирование и манипулирование Jupyter notebooks (.ipynb). Используйте при работе с ноутбуками, анализе данных, ML экспериментах.
---

# IPYNB Notebook Skill

Эксперт по созданию, редактированию и манипулированию Jupyter notebooks программно.

## Структура Notebook

Файл `.ipynb` — это JSON следующей структуры:

```json
{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {"provenance": []},
    "kernelspec": {"name": "python3", "display_name": "Python 3"}
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": ["line 1\n", "line 2\n"],
      "metadata": {"id": "unique_id"}
    }
  ]
}
```

## Ключевые правила

### Формат source ячеек
- `source` — это **массив строк**, каждая заканчивается на `\n` (кроме, возможно, последней)
- НЕ одна строка
- Пример: `["print('hello')\n", "print('world')\n"]`

### Экранирование в JSON
При записи JSON ноутбука:
- Кавычки: `\"`
- Символ новой строки: `\\n` (литерал) vs `\n` (реальный перенос в массиве)
- Обратные слеши: `\\`

### ID ячеек
- Каждая ячейка нуждается в уникальном `metadata.id`
- Используйте описательные ID: `"install_deps"`, `"train_model"`, `"plot_results"`

## Создание ноутбуков

### Markdown ячейки
```python
{
    "cell_type": "markdown",
    "source": [
        "# My Notebook\n",
        "\n",
        "Описание здесь.\n"
    ],
    "metadata": {"id": "intro"}
}
```

### Code ячейки
```python
{
    "cell_type": "code",
    "source": [
        "import torch\n",
        "import numpy as np\n",
        "\n",
        "print('Ready!')\n"
    ],
    "metadata": {"id": "imports"},
    "execution_count": null,
    "outputs": []
}
```

### Colab Form поля
```python
"#@title Заголовок ячейки { display-mode: \"form\" }\n",
"param = \"default\"  #@param {type:\"string\"}\n",
"number = 10  #@param {type:\"integer\"}\n",
"flag = True  #@param {type:\"boolean\"}\n",
"choice = \"A\"  #@param [\"A\", \"B\", \"C\"]\n",
```

### Складывающиеся секции (Colab)
Используйте `#@title` на code ячейках — они становятся складываемыми после запуска.

## Редактирование ноутбуков

### Паттерн безопасного редактирования
```python
import json

# Чтение
with open('notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Поиск ячейки по ID
for cell in nb['cells']:
    if cell.get('metadata', {}).get('id') == 'target_id':
        # Модификация cell['source']
        break

# Запись обратно
with open('notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
```

### Вставка ячейки
```python
new_cell = {
    "cell_type": "code",
    "source": ["# новый код\n"],
    "metadata": {"id": "new_cell"},
    "execution_count": null,
    "outputs": []
}
# Вставка по позиции
nb['cells'].insert(index, new_cell)
```

### Удаление ячейки
```python
nb['cells'] = [c for c in nb['cells'] if c.get('metadata', {}).get('id') != 'cell_to_delete']
```

## Паттерны ноутбуков

### Ячейка настройки (распространённая)
```python
["#@title Setup\n",
 "!pip install -q package1 package2\n",
 "\n",
 "import package1\n",
 "import package2\n",
 "\n",
 "print('✓ Setup complete')\n"]
```

### Ячейка конфигурации (Colab Forms)
```python
["#@title Configuration { display-mode: \"form\" }\n",
 "\n",
 "MODEL_NAME = \"gpt2\"  #@param {type:\"string\"}\n",
 "BATCH_SIZE = 32  #@param {type:\"integer\"}\n",
 "USE_GPU = True  #@param {type:\"boolean\"}\n"]
```

### Отображение прогресса
```python
["from tqdm.notebook import tqdm\n",
 "\n",
 "for i in tqdm(range(100)):\n",
 "    # работа\n",
 "    pass\n"]
```

## Чек-лист качества

Перед финализацией ноутбука:
- [ ] Все ячейки имеют уникальные ID
- [ ] Markdown ячейки имеют правильные заголовки и форматирование
- [ ] Code ячейки логически упорядочены
- [ ] Импорты в начале или в ячейке setup
- [ ] Значения конфигурации используют Colab form поля где уместно
- [ ] Обработка ошибок для распространённых сбоев
- [ ] Понятные сообщения вывода (✓ для успеха, ⚠️ для предупреждений)
- [ ] Разделители секций между основными частями

## Скрипты

Для продвинутого использования см. `scripts/nb_helper.py` — утилита для быстрого редактирования ноутбуков.
