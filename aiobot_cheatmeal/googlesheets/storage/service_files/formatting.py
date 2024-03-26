from typing import Dict

format_a1_a2_cell = {
    'horizontalAlignment': 'CENTER',
    'backgroundColor': {
        'red': 0.005,
        'green': 0.855,
        'blue': 0.304,
    },
    "textFormat": {
        'bold': True
    }
}

format_center = {
    'horizontalAlignment': 'CENTER',
    'wrapStrategy': 'WRAP',
}

format_center_middle = {
    'horizontalAlignment': 'CENTER',
    'wrapStrategy': 'WRAP',
    'verticalAlignment': 'MIDDLE',
}

format_OVERFLOW_CELL = {
    'wrapStrategy': 'OVERFLOW_CELL',
}

# Применяем форматирование к ячейкам с A1 по B2 (пример)
cell_border_format = {
    "borders": {
        "top": {
            "style": "SOLID",
            "width": 1,
            "color": {"red": 0.0, "green": 0.0, "blue": 0.0}
        },
        "bottom": {
            "style": "SOLID",
            "width": 1,
            "color": {"red": 0.0, "green": 0.0, "blue": 0.0}
        },
        "left": {
            "style": "SOLID",
            "width": 1,
            "color": {"red": 0.0, "green": 0.0, "blue": 0.0}
        },
        "right": {
            "style": "SOLID",
            "width": 1,
            "color": {"red": 0.0, "green": 0.0, "blue": 0.0}
        }
    }
}
