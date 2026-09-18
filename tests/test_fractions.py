from fractions import Fraction

import pytest

from braidge_tools.fractions import add_inches, format_inches, parse_inches, snap_inches, subtract_inches


def test_parse_common_shop_fractions():
    assert parse_inches("55 3/8") == Fraction(443, 8)
    assert parse_inches('1/16"') == Fraction(1, 16)
    assert parse_inches("2.5 in") == Fraction(5, 2)


def test_format_rounds_to_denominator():
    assert format_inches(Fraction(443, 8)) == "55 3/8"
    assert format_inches(Fraction(-3, 2)) == "-1 1/2"
    assert format_inches("1.03", denominator=16) == "1"


def test_exact_arithmetic():
    assert add_inches("35 3/8", "53 3/8") == Fraction(355, 4)
    assert subtract_inches("96", "25 1/2") == Fraction(141, 2)
    assert snap_inches("1.07") == Fraction(17, 16)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        parse_inches("about 4")
