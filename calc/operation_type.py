from enum import Enum
from typing import Callable, Any

from calc.calculator_service import CalculatorService

type OperationRef = Callable[[CalculatorService, Any, Any], Any]

class OperationType(str, Enum):
    """Перечисление для API, представляющий арифметическую операцию"""

    ADD = ("add", CalculatorService.add)
    SUBTRACT = ("subtract", CalculatorService.subtract)
    MULTIPLY = ("multiply", CalculatorService.multiply)
    DIVIDE = ("divide", CalculatorService.divide)

    def __new__(cls, str_value: str, operation_ref: OperationRef):
        obj = str.__new__(cls, str_value)
        obj._value_ = str_value
        obj._operation_ref = operation_ref
        return obj

    @property
    def operation_ref(self) -> OperationRef:
        """Свойство, возвращающее ссылку на реализацию арифметической операции"""
        return self._operation_ref

    def execute(self, service: CalculatorService, a, b):
        """Вызывает реализацию арифметической операции для указанных операндов, используя service"""
        return self.operation_ref(service, a, b)

