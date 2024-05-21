"""Структуры для представления товаров"""

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class Item(BaseModel):
    """Товар"""

    ident: str = Field(str, min_length=1)
    order_date: date
    name: str = Field(str, min_length=1)
    category_name: str = Field(str, min_length=1)
    sales_count: int = Field(int, gt=0)
    price: int = Field(int, gt=0)
    total_cost: int = Field(int, gt=0)

    @field_validator("order_date", mode="after")
    @classmethod
    def order_date_not_in_future(cls, value: date):
        """Валидирует, что дата не находится в будущем"""
        if value > datetime.now().date():
            raise ValueError("Order date is in the future")
        return value

    @field_validator("order_date", mode="before")
    @classmethod
    def parse_order_date(cls, value: str) -> date:
        """Валидирует, что дата в правильном формате"""
        return datetime.strptime(value, "%d.%m.%Y").date()

    @field_validator("total_cost", mode="after")
    @classmethod
    def parse_total_cost(cls, value: int, info: FieldValidationInfo):
        """Валидирует, что сумма произведений количества продаж на цену равняется общей выручке"""
        if info.data["sales_count"] * info.data["price"] != value:
            raise ValueError("sales_count * price != total_cost")
        return value

    def __str__(self):
        return f"{self.name} (ident: {self.ident})"


class Items(BaseModel):
    """Товары"""

    items: list[Item]

    @field_validator("items", mode="after")
    @classmethod
    def unique_idents(cls, value: list[Item]):
        """Валидирует, что в коллекции товаров не встречаются товары с одинаковыми
        идентификаторами"""
        if len(value) != len(set(map(lambda x: x.ident, value))):
            raise ValueError("Unique identifiers constraint violation")
        return value
