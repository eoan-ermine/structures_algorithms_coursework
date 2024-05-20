"""Вспомогательные функции для работы с столбцами"""


def get_column_titles():
    """Возвращает словарь, ставящий в соответствие названиям столбцов их внутренние '''
    идентификаторы"""
    return {
        "Номер заказа": "ident",
        "Дата заказа": "order_date",
        "Название товара": "name",
        "Категория товара": "category_name",
        "Количество продаж": "sales_count",
        "Цена за единицу": "price",
        "Общая стоимость": "total_cost",
    }


def validate_column_titles(row: dict[str, str]):
    """Валидирует столбцы в строке"""
    headers = get_column_titles()
    if list(row.keys()) != list(headers.keys()):
        raise ValueError("Wrong column titles")
    return row


def normalize_columns(rows: list[dict[str, str]]):
    """Нормализует строки, переводя ключи в внутренний формат"""
    headers = get_column_titles()
    rows = [{headers[k]: v for k, v in row.items()} for row in rows]
    return rows
