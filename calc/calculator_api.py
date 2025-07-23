from fastapi import APIRouter, Depends, Query, Path

from calc.api_respone import ValueErrorDetail, CalculatorResult
from calc.calculator_service import CalculatorService
from calc.operand_type import OperandType
from calc.operation_type import OperationType

router = APIRouter()

def get_calculator_service(
        operand_type: OperandType = Path(
        ...,  # Указываем, что параметр обязательный
        description = "Числовой тип операндов, используемых в вычислении.",
        example = OperandType.FLOAT.value  # Лучше использовать значение из Enum для примера
    )
    ) -> CalculatorService:
    return operand_type.create_service()

@router.get(
    "/{operand_type}/{operation_type}",
    summary = "Выполняет арифметические действия над числами",
    description = "Выполняет одну из четырех арифметических операций над двумя операндами",
    responses = {
        200: {
            "model": CalculatorResult,
            "description": "результат арифметического действия"
        },
        400: {
            "model": ValueErrorDetail,
            "description": "ошибка входных данных (например, деление на ноль или некорректный формат числа)"
        }
    }
)
async def calculate(
    a: str = Query(..., description = "первый операнд операции", example = "1"),
    b: str = Query(..., description = "второй операнд операции", example = "2"),
    operand_type: OperandType = Path(...),  # заглушка, чтобы сохранить логический порядок
    operation_type: OperationType = Path(..., description = "арифметическая операция", example = OperationType.ADD.value),
    service: CalculatorService = Depends(get_calculator_service)):

    typed_a, typed_b = operand_type.parse_value(a), operand_type.parse_value(b)
    result_value = operation_type.execute(service, typed_a, typed_b)

    return CalculatorResult.of(result_value)
