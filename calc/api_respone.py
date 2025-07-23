from typing import Union, Any, Self

from pydantic import BaseModel, Field

class CalculatorResult(BaseModel):
    """Объект с результатом арифметического действия"""
    result: Union[str, float, int] = Field(
        ...,
        description = "Результат арифметической операции. Для Decimal-типов всегда возвращается в виде строки для сохранения точности."
    )

    @classmethod
    def of(cls, result_value: Any) -> Self:
        if not isinstance(result_value, (int, float)):
            result_value = str(result_value)
        return cls(
            result = result_value
        )

class ValueErrorDetail(BaseModel):
    """Объект с описанием ошибки входных данных"""
    error_type: str = Field(
        ...,
        description = "Тип ошибки (наименование исключения)."
    )
    message: str = Field(
        ...,  # Три точки означают, что поле является обязательным
        description = "Сообщение с описанием проблемы."
    )

    @classmethod
    def of(cls, value_error: ValueError) -> Self:
        return cls(
            error_type = value_error.__class__.__name__,
            message = str(value_error)
        );
