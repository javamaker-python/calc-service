from decimal import Decimal, InvalidOperation
from typing import Type

from fastapi import APIRouter, Depends, HTTPException

from calc.calculator_service import CalculatorService
from calc.operand_type import OperandType

def _parse_operands(a: str, b: str, operand_type: OperandType):
    """Вспомогательная функция для DRY (Don't Repeat Yourself)"""
    try:
        return operand_type.parse_value(a), operand_type.parse_value(b)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

def get_calculator_service(operand_type: OperandType) -> CalculatorService:
    return operand_type.create_service()

router = APIRouter()

@router.get("/{operand_type}/add")
def add(a: str, b: str, operand_type: OperandType, calculator: CalculatorService = Depends(get_calculator_service)):
    typed_a, typed_b = _parse_operands(a, b, operand_type)
    result = calculator.add(typed_a, typed_b)
    return {"result": str(result) if isinstance(result, Decimal) else result}
