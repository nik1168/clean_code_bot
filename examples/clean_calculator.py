"""Basic arithmetic calculator with dispatch-based operation routing."""

import math


class Calculator:
    """Runs arithmetic operations via a string-keyed dispatch table.

    Supports: add, sub, mul, div, pow, sqrt, mod.
    """

    def compute(self, a, b, operation):
        """Execute the given operation on a and b.

        Args:
            a: first operand (also the sole operand for sqrt).
            b: second operand.
            operation: string key like "add", "div", etc.

        Raises:
            ValueError: for division/mod by zero or negative sqrt.
            KeyError: if the operation isn't recognised.
        """
        ops = {
            "add": lambda: a + b,
            "sub": lambda: a - b,
            "mul": lambda: a * b,
            "div": lambda: self._safe_div(a, b),
            "pow": lambda: a ** b,
            "sqrt": lambda: self._safe_sqrt(a),
            "mod": lambda: self._safe_mod(a, b),
        }
        if operation not in ops:
            raise KeyError(f"Unknown operation: '{operation}'")
        return ops[operation]()

    @staticmethod
    def _safe_div(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def _safe_sqrt(a):
        if a < 0:
            raise ValueError("Cannot take sqrt of a negative number")
        return math.sqrt(a)

    @staticmethod
    def _safe_mod(a, b):
        if b == 0:
            raise ValueError("Cannot mod by zero")
        return a % b


if __name__ == "__main__":
    c = Calculator()
    print(c.compute(10, 5, "add"))      # 15
    print(c.compute(25, 0, "sqrt"))     # 5.0
    print(c.compute(2, 10, "pow"))      # 1024
    print(c.compute(10, 3, "mod"))      # 1

    # should raise
    try:
        c.compute(10, 0, "div")
    except ValueError as e:
        print(f"caught: {e}")
