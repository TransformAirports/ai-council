from __future__ import annotations

import math
import unittest

from cli.server import _coerce_budget


class ServerBudgetTests(unittest.TestCase):
    def test_zero_is_preserved(self) -> None:
        self.assertEqual(_coerce_budget(0), 0.0)
        self.assertEqual(_coerce_budget("0"), 0.0)

    def test_blank_is_unlimited(self) -> None:
        self.assertIsNone(_coerce_budget(None))
        self.assertIsNone(_coerce_budget(""))

    def test_invalid_values_are_rejected(self) -> None:
        for value in (-1, "nope", math.nan, math.inf, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _coerce_budget(value)


if __name__ == "__main__":
    unittest.main()
