"""Основной модуль программы, предоставляющий CLI интерфейс"""

import csv
import os.path
import sys

import typer
from pydantic import ValidationError

from .structures import Item, Items
from .utils import normalize_columns, validate_column_titles


def print_report(items: list[Item], f):
    """Печатает в переданный файл отчет по переданным товарам"""
    total_income = sum(map(lambda x: x.total_cost, items))
    print(f"Total income: {total_income}", file=f)
    bestseller = max(items, key=lambda x: x.sales_count)
    print(f"Bestseller: {bestseller}", file=f)
    most_income_product = max(items, key=lambda x: x.total_cost)
    print(f"Most income product: {most_income_product}", file=f)
    print("Structure of the income:", file=f)
    items.sort(key=lambda x: -x.total_cost)
    for i, item in enumerate(items):
        print(f"{i + 1}) {item} — {item.total_cost / total_income * 100}% of total income", file=f)


def main(path: str):
    """Entrypoint для работы typer"""
    if not os.path.isfile(path):
        print(f"{path} is not a file")
        raise typer.Exit(code=1)

    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="|", skipinitialspace=True)

        try:
            items = [validate_column_titles(row) for row in reader]
        except ValueError as e:
            print(f"Columns validation error: {e}")
            raise typer.Exit(1)

        items = normalize_columns(items)

        try:
            items = Items(**{"items": [Item(**row) for row in items]}).items
        except ValidationError as e:
            print(f"Row validation error: {e}")
            raise typer.Exit(code=1)

        print_report(items, sys.stdout)


if __name__ == "__main__":
    typer.run(main)
