from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import pytest

from calc import calculator_api
from calc.api_respone import ValueErrorDetail
from main import  value_error_exception_handler

app = FastAPI()
app.include_router(calculator_api.router)
app.add_exception_handler(ValueError, value_error_exception_handler)
client = TestClient(app)

_invalid_input = [
    # сложение
    ("add", "integer", "abc"),
    ("add", "float", "abc"),
    ("add", "decimal", "abc"),
    # вычитание
    ("subtract", "integer", "abc"),
    ("subtract", "float", "abc"),
    ("subtract", "decimal", "abc"),
    # умножение
    ("multiply", "integer", "abc"),
    ("multiply", "float", "abc"),
    ("multiply", "decimal", "abc"),
    # деление
    ("divide", "integer", "abc"),
    ("divide", "float", "abc"),
    ("divide", "decimal", "abc")
]

class TestCalculate:
    """/{operand_type}/add"""

    @pytest.mark.parametrize(
        ("operation_type", "operand_type", "a", "b", "expected_value"), [
            pytest.param(operation_type, operand_type, a, b, expected_value,
                         id = f"/{operand_type}/{operation_type}?a={a}&b={b} => [200] {expected_value}")
            for operation_type, operand_type, a, b, expected_value in [
                # сложение
                ("add", "integer", "5", "10", 15),
                ("add", "float", "1.5", "2.75", 4.25),
                ("add", "decimal", "1.5", "2.75", "4.25"),
                # вычитание
                ("subtract", "integer", "-5", "-10", 5),
                ("subtract", "float", "1.5", "2.75", -1.25),
                ("subtract", "decimal", "0.0", "-5.5", "5.5"),
                # умножение
                ("multiply", "integer", "10", "-20", -200),
                ("multiply", "float", "100", "0.123", 12.3),
                ("multiply", "decimal", "-10.1", "2.0", "-20.20"),
                # деление
                ("divide", "integer", "101", "-20", -5),
                ("divide", "float", "4.5", "1.5", 3.0),
                ("divide", "decimal", "100", "12.5", "8")
        ]
    ])
    def test_result(self, operation_type, operand_type, a, b, expected_value):
        """тест на выполнение арифметических операций черех API"""

        response = client.get(f"/{operand_type}/{operation_type}?a={a}&b={b}")
        assert response.status_code == 200
        assert response.json() == {"result": expected_value}

    @pytest.mark.parametrize(
        ("operation_type", "operand_type", "a"), [
            pytest.param(operation_type, operand_type, a,
                         id = f"/{operand_type}/{operation_type}?a={a}&b=1 => [400]")
            for operation_type, operand_type, a in _invalid_input
    ])
    def test_invalid_a(self, operation_type, operand_type, a):
        """тест на проверку первого операнда"""

        response = client.get(f"/{operand_type}/{operation_type}?a={a}&b=1")
        self._verify_invalid_value(response, f"{a}")

    @pytest.mark.parametrize(
        ("operation_type", "operand_type", "b"), [
            pytest.param(operation_type, operand_type, b,
                         id = f"/{operand_type}/{operation_type}?a=1&b={b} => [400]")
            for operation_type, operand_type, b in _invalid_input
    ])
    def test_invalid_b(self, operation_type, operand_type, b):
        """тест на проверку второго операнда"""

        response = client.get(f"/{operand_type}/{operation_type}?a=1&b={b}")
        self._verify_invalid_value(response, f"{b}")

    def _verify_invalid_value(self, response, invalid_value: str):
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response_data: ValueErrorDetail = ValueErrorDetail.model_validate(response.json())
        assert response_data.error_type == "ValueError"

        message = response_data.message
        assert "невозможно преобразовать значение" in message
        assert invalid_value in message
