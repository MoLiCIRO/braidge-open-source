"""Generic cutout validation for countertop fabrication tools."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from math import hypot
from typing import Literal

from braidge_tools.geometry import Point, bounds, point_in_polygon

CutoutKind = Literal["sink", "cooktop", "grommet", "faucet", "custom"]


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Cutout:
    kind: CutoutKind
    x: float
    y: float
    width: float
    height: float | None = None
    label: str | None = None

    @property
    def is_round(self) -> bool:
        return self.height is None

    @property
    def radius(self) -> float:
        if not self.is_round:
            raise ValueError("rectangular cutout does not have a radius")
        return self.width / 2.0

    @property
    def half_width(self) -> float:
        return self.width / 2.0

    @property
    def half_height(self) -> float:
        return (self.height if self.height is not None else self.width) / 2.0


@dataclass(frozen=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    cutout: Cutout | None = None


def validate_cutouts(
    outline: Iterable[Point | tuple[float, float]],
    cutouts: Iterable[Cutout],
    *,
    min_edge_clearance: float = 2.0,
    min_between_cutouts: float = 1.0,
) -> list[ValidationIssue]:
    """Validate generic cutout placement against a simple countertop outline.

    Clearance defaults are illustrative and configurable, not universal
    fabrication standards. Use material-, equipment-, and shop-specific
    requirements for production decisions.
    """

    polygon = list(outline)
    openings = list(cutouts)
    min_x, min_y, max_x, max_y = bounds(polygon)
    issues: list[ValidationIssue] = []

    for cutout in openings:
        if cutout.width <= 0 or (cutout.height is not None and cutout.height <= 0):
            issues.append(
                ValidationIssue(Severity.ERROR, "invalid-size", "Cutout dimensions must be positive.", cutout)
            )
            continue

        corners = _cutout_sample_points(cutout)
        if not all(point_in_polygon(point, polygon) for point in corners):
            issues.append(
                ValidationIssue(Severity.ERROR, "outside-outline", "Cutout extends outside the countertop outline.", cutout)
            )

        clearance = min(
            cutout.x - cutout.half_width - min_x,
            max_x - (cutout.x + cutout.half_width),
            cutout.y - cutout.half_height - min_y,
            max_y - (cutout.y + cutout.half_height),
        )
        if clearance < min_edge_clearance:
            issues.append(
                ValidationIssue(
                    Severity.WARNING,
                    "edge-clearance",
                    f"Cutout is {clearance:.2f} inches from the bounding edge.",
                    cutout,
                )
            )

    for left_index, left in enumerate(openings):
        for right in openings[left_index + 1 :]:
            gap = cutout_gap(left, right)
            if gap < min_between_cutouts:
                issues.append(
                    ValidationIssue(
                        Severity.WARNING,
                        "cutout-spacing",
                        f"Cutouts are {gap:.2f} inches apart.",
                        left,
                    )
                )

    return issues


def cutout_gap(a: Cutout, b: Cutout) -> float:
    dx = max(abs(a.x - b.x) - a.half_width - b.half_width, 0.0)
    dy = max(abs(a.y - b.y) - a.half_height - b.half_height, 0.0)
    return hypot(dx, dy)


def _cutout_sample_points(cutout: Cutout) -> list[Point]:
    return [
        Point(cutout.x - cutout.half_width, cutout.y - cutout.half_height),
        Point(cutout.x + cutout.half_width, cutout.y - cutout.half_height),
        Point(cutout.x + cutout.half_width, cutout.y + cutout.half_height),
        Point(cutout.x - cutout.half_width, cutout.y + cutout.half_height),
    ]
