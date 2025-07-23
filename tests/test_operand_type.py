from decimal import Decimal

import pytest

from calc.calculator_service import CalculatorService
from calc.operand_type import OperandType

def declare_params_for_result():
    """метод-помощник, объявляет имена параметров для тестов с проверкой на результат"""
    return ("input_value", "expected_output")

def declare_params_for_exception():
    """метод-помощник, объявляет имена параметры для тестов с проверкой на исключение"""
    return ("input_value")

def define_params_for_result(data_list) -> list[pytest.param]:
    """метод-помощник, формирует для теста с проверкой на результат список pytest.param из данных"""
    return [
        pytest.param(input_value, expected_output,
                     id = f"{type(input_value)}({input_value}) => {type(expected_output)}({expected_output})")
        for input_value, expected_output in data_list
    ]

def define_params_for_exception(data_list) -> list[pytest.param]:
    """метод-помощник, формирует для теста с проверкой на исключение список pytest.param из данных"""
    return [
        pytest.param(input_value, id = f"{type(input_value)}({input_value}) => ValueError")
        for input_value in data_list
    ]

class TestOperandType:
    """OperandType"""

    @pytest.mark.parametrize("operand_type", [
        OperandType.INTEGER,
        OperandType.FLOAT,
        OperandType.DECIMAL
    ])
    def test_create_service(self, operand_type):
        service = operand_type.create_service()
        assert isinstance(service, CalculatorService)

class TestOperandTypeForInteger:
    """OperandType.INTEGER"""

    @pytest.fixture
    def operand_type(self):
        return OperandType.INTEGER

    def test_numeric_type(self, operand_type):
        assert operand_type.numeric_type == int

    def test_service_class(self, operand_type):
        assert operand_type.service_class == CalculatorService[int];

    @pytest.mark.parametrize(declare_params_for_result(), define_params_for_result([
        ("555", 555),
        (float(2.5), 2),
        (Decimal(2), 2),
        (11, 11)
    ]))
    def test_parse_value(self, operand_type, input_value, expected_output):
        assert operand_type.parse_value(input_value) == expected_output;

    @pytest.mark.parametrize(declare_params_for_exception(), define_params_for_exception([
        ("555.0"),
        ("aaa")
    ]))
    def test_parse_invalid_value(self, operand_type, input_value):
        with pytest.raises(ValueError) as e:
            operand_type.parse_value(input_value)
        assert "невозможно преобразовать значение" in str(e)

class TestOperandTypeForFloat:
    """OperandType.FLOAT"""

    @pytest.fixture
    def operand_type(self):
        return OperandType.FLOAT

    def test_numeric_type(self, operand_type):
        assert operand_type.numeric_type == float

    def test_service_class(self, operand_type):
        assert operand_type.service_class == CalculatorService[float];

    @pytest.mark.parametrize(declare_params_for_result(), define_params_for_result([
        ("555", 555.0),
        (float(2.5), 2.5),
        (Decimal(2), 2.0),
        (11, 11.0)
    ]))
    def test_parse_value(self, operand_type, input_value, expected_output):
        assert operand_type.parse_value(input_value) == expected_output;

    @pytest.mark.parametrize(declare_params_for_exception(), define_params_for_exception([
        ("aaa"), ("")
    ]))
    def test_parse_invalid_value(self, operand_type, input_value):
        with pytest.raises(ValueError) as e:
            operand_type.parse_value(input_value)
        assert "невозможно преобразовать значение" in str(e)

class TestOperandTypeForDecimal:
    """OperandType.DECIMAL"""

    @pytest.fixture
    def operand_type(self):
        return OperandType.DECIMAL

    def test_numeric_type(self, operand_type):
        assert operand_type.numeric_type == Decimal

    def test_service_class(self, operand_type):
        assert operand_type.service_class == CalculatorService[Decimal];

    @pytest.mark.parametrize(declare_params_for_result(), define_params_for_result([
        ("555", Decimal(555)),
        (float(2.5), Decimal(2.5)),
        (Decimal(2), Decimal(2)),
        (11, Decimal(11))
    ]))
    def test_parse_value(self, operand_type, input_value, expected_output):
        assert operand_type.parse_value(input_value) == expected_output;

    @pytest.mark.parametrize(declare_params_for_exception(), define_params_for_exception([
        ("aaa"), ("")
    ]))
    def test_parse_invalid_value(self, operand_type, input_value):
        with pytest.raises(ValueError) as e:
            operand_type.parse_value(input_value)
        assert "невозможно преобразовать значение" in str(e)

