"""Inch fraction parsing and formatting helpers."""

from __future__ import annotations

import re
from fractions import Fraction

INCH_MARKS = ('"', "in", "inch", "inches")
_MIXED_RE = re.compile(r"^(?P<whole>[+-]?\d+)\s+(?P<num>\d+)\s*/\s*(?P<den>\d+)$")
_FRACTION_RE = re.compile(r"^(?P<num>[+-]?\d+)\s*/\s*(?P<den>\d+)$")
_DECIMAL_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")


def parse_inches(value: str | float | Fraction | None) -> Fraction:
    """Parse an inch value into an exact Fraction."""

    if value is None:
        raise ValueError("inch value is required")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, float):
        return Fraction(str(value))

    text = str(value).strip().lower()
    if not text:
        raise ValueError("inch value is empty")
    for mark in INCH_MARKS:
        if text.endswith(mark):
            text = text[: -len(mark)].strip()
            break
    text = text.replace("−", "-").replace("'", "").strip()

    mixed = _MIXED_RE.match(text)
    if mixed:
        whole = int(mixed.group("whole"))
        frac = Fraction(int(mixed.group("num")), int(mixed.group("den")))
        return Fraction(whole, 1) - frac if whole < 0 else Fraction(whole, 1) + frac

    simple = _FRACTION_RE.match(text)
    if simple:
        return Fraction(int(simple.group("num")), int(simple.group("den")))

    if _DECIMAL_RE.match(text):
        return Fraction(text)

    raise ValueError(f"could not parse inch value: {value!r}")


def snap_inches(value: str | float | Fraction, increment: Fraction = Fraction(1, 16)) -> Fraction:
    parsed = parse_inches(value)
    if increment <= 0:
        raise ValueError("increment must be positive")
    return round(parsed / increment) * increment


def format_inches(value: str | float | Fraction, denominator: int = 16) -> str:
    if denominator <= 0:
        raise ValueError("denominator must be positive")

    rounded = snap_inches(parse_inches(value), Fraction(1, denominator))
    sign = "-" if rounded < 0 else ""
    rounded = abs(rounded)
    whole = rounded.numerator // rounded.denominator
    remainder = rounded - whole

    if remainder == 0:
        return f"{sign}{whole}"
    if whole == 0:
        return f"{sign}{remainder.numerator}/{remainder.denominator}"
    return f"{sign}{whole} {remainder.numerator}/{remainder.denominator}"


def add_inches(*values: str | float | Fraction) -> Fraction:
    return sum((parse_inches(value) for value in values), Fraction(0, 1))


def subtract_inches(first: str | float | Fraction, *rest: str | float | Fraction) -> Fraction:
    return parse_inches(first) - add_inches(*rest)
