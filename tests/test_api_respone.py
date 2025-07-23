from decimal import Decimal

from calc.api_respone import CalculatorResult, ValueErrorDetail

class TestCalculatorResult:

    def test_of_int(self):
        obj = CalculatorResult.of(5)

        assert type(obj.result) == int
        assert obj.result == 5

    def test_of_float(self):
        obj = CalculatorResult.of(22.0)

        assert type(obj.result) == float
        assert obj.result == 22.0

    def test_of_decimal(self):
        obj = CalculatorResult.of(Decimal("5.7"))

        assert type(obj.result) == str
        assert obj.result == "5.7"

class TestValueErrorDetail:

    def test_of(self):
        err = ValueError("test error");
        obj = ValueErrorDetail.of(err)

        assert obj.error_type == "ValueError"
        assert obj.message == "test error"
