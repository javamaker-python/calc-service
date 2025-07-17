'''
Created on 16 июл. 2025 г.

@author: yushin
'''
from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class CalculatorOperand(Protocol):

    def __add__(self, other) -> Self: ...

    def __sub__(self, other) -> Self: ...

    def __mul__(self, other) -> Self: ...

    def __truediv__(self, other) -> Self: ...


class CalculatorService[T: CalculatorOperand]():

    def _validate_operands(self, a: T, b: T):
        if not a:
            raise ValueError("первый операнд не может быть пустым")
        if not isinstance(a, CalculatorOperand):
            raise ValueError(f"первый операнд содержит некорректное значение '{a}', ожидаем число")

        if not b:
            raise ValueError("второй операнд не может быть пустым")
        if not isinstance(b, CalculatorOperand):
            raise ValueError(f"второй операнд содержит некорректное значение '{b}', ожидаем число")

    def add(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return a + b

    def subtract(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return a - b

    def multiply(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return a * b

    def divide(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return a / b
    