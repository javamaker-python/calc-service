'''
Created on 18 июл. 2025 г.

@author: yushin
'''
from typing import runtime_checkable, Protocol, Self

@runtime_checkable
class CalculatorOperand(Protocol):

    def __add__(self, other) -> Self: ...

    def __sub__(self, other) -> Self: ...

    def __mul__(self, other) -> Self: ...

    def __truediv__(self, other) -> Self: ...
