'''
Created on 16 июл. 2025 г.

@author: yushin
'''
import math
import pytest
from decimal import Decimal
from calc.calculator_service import CalculatorService

def declare_params_for_result():
    """метод-помощник, объявляет имена параметров для тестов с проверкой на результат"""
    return ("a", "b", "expected")

def declare_params_for_exception():
    """метод-помощник, объявляет имена параметры для тестов с проверкой на исключение"""
    return ("a", "b")

def define_params_for_result(data_list, id_format) -> list[pytest.param]:
    """метод-помощник, формирует для теста с проверкой на результат список pytest.param из данных"""
    return [
        pytest.param(a, b, expected, id=id_format.format(a=a, b=b, expected=expected))
        for a, b, expected in data_list
    ]

def define_params_for_exception(data_list) -> list[pytest.param]:
    """метод-помощник, формирует для теста с проверкой на исключение список pytest.param из данных"""
    return [
        pytest.param(a, b, id=f"{a} / {b} => ValueError")
        for a, b in data_list
    ]

class TestCalculatorService:
    """CalculatorService"""

    @pytest.fixture
    def service(self):
        return CalculatorService()

    class TestAdd:
        """add(a, b)"""

        @staticmethod
        def _define_add_params(data_list) -> list[pytest.param]:
            return define_params_for_result(data_list, "{a} + {b} => {expected}")

        @pytest.mark.parametrize(declare_params_for_result(), _define_add_params([
            (0, 0, 0),
            (1, 2, 3),
            (0, 5, 5),
            (-1, 10, 9)
        ]))
        def test_int(self, service, a, b, expected):
            """тест на сложение целых чисел"""
            assert service.add(a, b) == expected
            assert service.add(b, a) == expected

        @pytest.mark.parametrize(declare_params_for_result(), _define_add_params([
            (0.0, 0.0, 0.0),
            (1.1, 2.2, 3.3),
            (0.0, 5.0, 5.0),
            (-0.5, 10.0, 9.5)
        ]))
        def test_float(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            math.isclose(service.add(a, b), expected)
            math.isclose(service.add(b, a), expected)

        @pytest.mark.parametrize(declare_params_for_result(), _define_add_params([
            (Decimal("0"), Decimal("0"), Decimal("0")),
            (Decimal("3.55"), Decimal("-1.55"), Decimal("2")),
            (Decimal("0"), Decimal("1.0"), Decimal("1.0"))
        ]))
        def test_decimal(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            assert service.add(a, b) == expected
            assert service.add(b, a) == expected

        @pytest.mark.parametrize(declare_params_for_exception(), define_params_for_exception([
            (None, 0),
            (0, None)
        ]))
        def test_none_input(self, service, a, b):
            with pytest.raises(ValueError) as err:
                service.add(a, b)
            assert "операнд не может быть пустым" in str(err.value)

        @pytest.mark.parametrize(declare_params_for_exception(), define_params_for_exception([
            ("aa", 0),
            (0, "bb")
        ]))
        def test_invalid_input(self, service, a, b):
            with pytest.raises(ValueError) as err:
                service.add(a, b)
            assert "операнд содержит некорректное значение" in str(err.value)
            
        @pytest.mark.parametrize(declare_params_for_exception(), define_params_for_exception([
            (0, 1.0),
            (Decimal(2), 5),
            (6.0, Decimal("7.7"))
        ]))
        def test_input_mismatch(self, service, a, b):
            with pytest.raises(ValueError) as err:
                service.add(a, b)
            assert "типы данных операндов различаются" in str(err.value)

#
    class TestSubtract:
        """subtract(a, b)"""

        @staticmethod
        def _define_subtract_params(data_list) -> list[pytest.param]:
            return define_params_for_result(data_list, "{a} - {b} => {expected}")

        @pytest.mark.parametrize(declare_params_for_result(), _define_subtract_params([
            (0, 0, 0),
            (1, 2, -1),
            (0, 5, -5),
            (-1, 10, -11)
        ]))
        def test_int(self, service, a, b, expected):
            """тест на сложение целых чисел"""
            assert service.subtract(a, b) == expected

        @pytest.mark.parametrize(declare_params_for_result(), _define_subtract_params([
            (0.0, 0.0, 0.0),
            (3.3, 2.2, 1.1),
            (0.0, 5.0, -5.0),
            (-0.5, 10.0, 10.5)
        ]))
        def test_float(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            math.isclose(service.subtract(a, b), expected)

        @pytest.mark.parametrize(declare_params_for_result(), _define_subtract_params([
            (Decimal("16"), Decimal("5"), Decimal("11")),
            (Decimal("0"), Decimal("-2"), Decimal("2"))
        ]))
        def test_decimal(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            math.isclose(service.subtract(a, b), expected)

    class TestMultiply:
        """multiply(a, b)"""

        @staticmethod
        def _define_multiply_params(data_list) -> list[pytest.param]:
            return define_params_for_result(data_list, "{a} * {b} => {expected}")

        @pytest.mark.parametrize(declare_params_for_result(), _define_multiply_params([
            (0, 0, 0),
            (1, 2, 2),
            (0, 5, 0),
            (-1, 10, -10)
        ]))
        def test_int(self, service, a, b, expected):
            """тест на сложение целых чисел"""
            assert service.multiply(a, b) == expected
            assert service.multiply(b, a) == expected

        @pytest.mark.parametrize(declare_params_for_result(), _define_multiply_params([
            (0.0, 1.0, 0.0),
            (1.1, 2.2, 2.22),
            (-0.5, 10.0, -5.0)
        ]))
        def test_float(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            math.isclose(service.multiply(a, b), expected)
            math.isclose(service.multiply(b, a), expected)

        @pytest.mark.parametrize(declare_params_for_result(), _define_multiply_params([
            (Decimal("30"), Decimal("0"), Decimal("0")),
            (Decimal("3.55"), Decimal("-2"), Decimal("-7.10"))
        ]))
        def test_decimal(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            assert service.multiply(a, b) == expected
            assert service.multiply(b, a) == expected

    class TestDivide:
        """divide(a, b)"""

        @staticmethod
        def _define_divide_params(data_list) -> list[pytest.param]:
            return define_params_for_result(data_list, "{a} / {b} => {expected}")

        @pytest.mark.parametrize(declare_params_for_result(), _define_divide_params([
            (0, 1, 0),
            (1, 2, 0),
            (5, 3, 1)
        ]))
        def test_int(self, service, a, b, expected):
            """тест на сложение целых чисел"""
            assert service.divide(a, b) == expected

        @pytest.mark.parametrize(declare_params_for_result(), _define_divide_params([
            (0.0, 0.1, 0.0),
            (3.3, 2.0, 1.65),
            (5.0, -2.0, -2.5)
        ]))
        def test_float(self, service, a, b, expected):
            """тест на сложение чисел с плавающей запятой"""
            math.isclose(service.divide(a, b), expected)

        @pytest.mark.parametrize(declare_params_for_result(), _define_divide_params([
            (Decimal("16"), Decimal("5"), Decimal("3.2")),
            (Decimal("0"), Decimal("-2"), Decimal("0"))
        ]))
        def test_decimal(self, service, a, b, expected):
            """тест на сложение целых чисел"""
            assert service.divide(a, b) == expected

        @pytest.mark.parametrize(("a", "b"), define_params_for_exception([
            (1, 0),
            (2.0, 0.0),
            (Decimal("3.00"), Decimal("0"))
        ]))
        def test_zero_division(self, service, a, b):
            with pytest.raises(ValueError) as err:
                service.divide(a, b)
            assert isinstance(err.value.args, tuple)
            assert "нельзя делить на ноль" in str(err.value.args[0])

