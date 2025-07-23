import math

import pytest

from calc.calculator_service import CalculatorService
from calc.operation_type import OperationType

class TestOperationType:
    """OperationType"""

    @pytest.fixture
    def service(self):
        return CalculatorService[int]()

    def test_add(self, service):
        """OperationType.ADD"""
        op = OperationType.ADD

        assert op.operation_ref == CalculatorService.add
        assert op.execute(service, 1, 2) == 3

    def test_subtract(self, service):
        """OperationType.SUBTRACT"""
        op = OperationType.SUBTRACT

        assert op.operation_ref == CalculatorService.subtract
        assert op.execute(service, 3, 2) == 1

    def test_multiply(self, service):
        """OperationType.MULTIPLY"""
        op = OperationType.MULTIPLY

        assert op.operation_ref == CalculatorService.multiply
        assert math.isclose(op.execute(service, 2.0, 3.00), 6.0)

    def test_divide(self, service):
        """OperationType.DIVIDE"""
        op = OperationType.DIVIDE

        assert op.operation_ref == CalculatorService.divide
        assert math.isclose(op.execute(service, 6.0, 3.0), 2.0)
