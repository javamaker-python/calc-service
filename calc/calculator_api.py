from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException

from calc.calculator_service import CalculatorService
from calc.operand_type import OperandType
from calc.operation_type import OperationType

def _parse_operands(a: str, b: str, operand_type: OperandType):
    """Вспомогательная функция для DRY (Don't Repeat Yourself)"""
    try:
        return operand_type.parse_value(a), operand_type.parse_value(b)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail = str(e))

def get_calculator_service(operand_type: OperandType) -> CalculatorService:
    return operand_type.create_service()

router = APIRouter()

@router.get("/{operand_type}/{operation_type}")
def calculate(a: str,
              b: str,
              operand_type: OperandType,
              operation_type: OperationType,
              service: CalculatorService = Depends(get_calculator_service)):
    typed_a, typed_b = _parse_operands(a, b, operand_type)
    result = operation_type.execute(service, typed_a, typed_b)
    return {"result": str(result) if isinstance(result, Decimal) else result}
