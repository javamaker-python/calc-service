'''
Created on 19 июл. 2025 г.

@author: yushin
'''
from decimal import Decimal
from enum import Enum

from fastapi.applications import FastAPI

from calc.calculator_service import CalculatorService

class OperandType(str, Enum):
    INTEGER = "integer"
    FLOAT = "float"
    DECIMAL = "decimal"

def calculator_service(operand_type: OperandType):
    if operand_type == OperandType.INTEGER:
        return CalculatorService[int]()
    if operand_type == OperandType.FLOAT:
        return CalculatorService[float]()
    if operand_type == OperandType.DECIMAL:
        return CalculatorService[Decimal]
    raise ValueError(f"неизвестный тип операндов {type}")

app = FastAPI()

class CalculatorApi(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
