from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Generic, Type, TypeVar

from calc.calculator_operand import CalculatorOperand
from calc.calculator_service import CalculatorService

O = TypeVar("O", bound = CalculatorOperand)

class OperandType(Generic[O], str, Enum):
    """Обобщенный Enum, представляющий тип операнда и действующий как фабрика."""

    def __new__(cls, str_value: str, service_class: CalculatorService[O], numeric_type: Type[O]):
        obj = str.__new__(cls, str_value)
        obj._value_ = str_value
        obj._service_class = service_class
        obj._numeric_type = numeric_type
        return obj

    # Определения элементов. Они конкретизируют тип O для каждого элемента.
    # Прямые кавычки нужны для "опережающей ссылки" (forward reference),
    # так как класс NumberType еще не до конца определен в этот момент.
    INTEGER: 'OperandType[int]' = ("integer", CalculatorService[int], int)
    FLOAT: 'OperandType[float]' = ("float", CalculatorService[float], float)
    DECIMAL: 'OperandType[Decimal]' = ("decimal", CalculatorService[Decimal], Decimal)

    @property
    def numeric_type(self) -> Type[O]:
        """Свойство, возвращающее класс числового типа (int, float или Decimal)."""
        return self._numeric_type

    @property
    def service_class(self) -> Type[CalculatorService[O]]:
        """Свойство, возвращающее тип CalculatorService, параметридованный выбранным числовым типом."""
        return self._service_class

    def create_service(self) -> 'CalculatorService[O]':
        """Фабричный метод для создания экземпляра сервиса."""
        return self.service_class()

    def parse_value(self, value: str) -> O:
        """
        Парсит входное значение в числовой тип, связанный с этим элементом Enum.
        Возвращаемый тип O будет корректно определен статическим анализатором.
        """
        try:
            return self.numeric_type(value)
        except (ValueError, InvalidOperation) as e:
            raise ValueError(f"невозможно преобразовать значение '{value}' в тип '{self.numeric_type.__name__}'") from e
