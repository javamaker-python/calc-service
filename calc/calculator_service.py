'''
Created on 16 июл. 2025 г.

@author: yushin
'''
from typing import Any
from calc.calculator_operand import CalculatorOperand

class CalculatorService[T: CalculatorOperand]():

    def _validate_operands(self, a: T, b: T):
        if a is None:
            raise ValueError("первый операнд не может быть пустым")
        if not isinstance(a, CalculatorOperand):
            raise ValueError(f"первый операнд содержит некорректное значение '{a}', ожидаем число")

        if b is None:
            raise ValueError("второй операнд не может быть пустым")
        if not isinstance(b, CalculatorOperand):
            raise ValueError(f"второй операнд содержит некорректное значение '{b}', ожидаем число")

        if type(a) != type(b):
            raise ValueError(f"типы данных операндов различаются: a => {type(a)}, b => {type(b)}")

    def _target_type(self, source: Any, target: T) -> T:
        target_type = type(target)
        return target_type(source)

    def add(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return self._target_type(a + b, a)

    def subtract(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return self._target_type(a - b, a)

    def multiply(self, a: T, b: T) -> T:
        self._validate_operands(a, b)
        return self._target_type(a * b, a)

    def divide(self, a: T, b: T) -> T:
        self._validate_operands(a, b)

        try:
            return self._target_type(a / b, a)
        except ZeroDivisionError as e:
            raise ValueError(f"нельзя делить на ноль: {a} / {b}!", e);
