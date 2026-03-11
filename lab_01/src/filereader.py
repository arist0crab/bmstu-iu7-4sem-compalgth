"""
Модуль для чтения и парсинга файла данных data.txt.
Все функции возвращают чистые данные без логики интерполяции.
"""


def read_all_data(filepath):
    """
    Главная функция модуля.
    Читает весь файл и возвращает словарь со всеми таблицами.

    Returns:
        dict: {
            'current': {
                'time': array[...],
                'current': array[...]
            },
            'nh': {
                'temperatures': array[...],
                'pressures': array[...],
                'values': 2D array[...]
            },
            'sigma': {...},
            'c': {...},
            'q': {...}
        }
    """
    pass


def _parse_current_table(lines, start_idx):
    """Парсит таблицу тока I(t). Возвращает индексы и данные."""
    pass


def _parse_2d_table(lines, start_idx, table_name):
    """
    Парсит двумерную таблицу (Nh, sigma, c, q).
    Возвращает:
        - массив температур
        - массив давлений
        - 2D массив значений
        - следующий индекс для чтения
    """
    pass


def _clean_line(line):
    """Очищает строку от лишних пробелов и спецсимволов."""
    pass