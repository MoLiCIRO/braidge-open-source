"""Small 2D geometry helpers for countertop-like outlines."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from math import hypot, isclose


@dataclass(frozen=True)
class Point:
    x: float
    y: float


def as_point(value: Point | Sequence[float]) -> Point:
    if isinstance(value, Point):
        return value
    if len(value) != 2:
        raise ValueError("point must contain exactly two coordinates")
    return Point(float(value[0]), float(value[1]))


def normalize_points(points: Iterable[Point | Sequence[float]]) -> list[Point]:
    return [as_point(point) for point in points]


ORIGIN = Point(0, 0)


def rectangle(width: float, height: float, origin: Point | Sequence[float] = ORIGIN) -> list[Point]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    base = as_point(origin)
    return [
        Point(base.x, base.y),
        Point(base.x + width, base.y),
        Point(base.x + width, base.y + height),
        Point(base.x, base.y + height),
    ]


def clipped_rectangle(width: float, height: float, *, clip: float, corner: str) -> list[Point]:
    if clip <= 0:
        raise ValueError("clip must be positive")
    if clip >= min(width, height):
        raise ValueError("clip must be smaller than both width and height")

    corners = {
        "bottom-left": [Point(clip, 0), Point(width, 0), Point(width, height), Point(0, height), Point(0, clip)],
        "bottom-right": [Point(0, 0), Point(width - clip, 0), Point(width, clip), Point(width, height), Point(0, height)],
        "top-right": [Point(0, 0), Point(width, 0), Point(width, height - clip), Point(width - clip, height), Point(0, height)],
        "top-left": [Point(0, 0), Point(width, 0), Point(width, height), Point(clip, height), Point(0, height - clip)],
    }
    try:
        return corners[corner]
    except KeyError as exc:
        raise ValueError(f"unsupported corner: {corner!r}") from exc


def close_outline(points: Iterable[Point | Sequence[float]]) -> list[Point]:
    outline = normalize_points(points)
    if not outline:
        return []
    if outline[0] != outline[-1]:
        outline.append(outline[0])
    return outline


def is_closed(points: Iterable[Point | Sequence[float]], tolerance: float = 1e-9) -> bool:
    outline = normalize_points(points)
    if len(outline) < 2:
        return False
    return distance(outline[0], outline[-1]) <= tolerance


def distance(a: Point | Sequence[float], b: Point | Sequence[float]) -> float:
    pa = as_point(a)
    pb = as_point(b)
    return hypot(pa.x - pb.x, pa.y - pb.y)


def edge_lengths(points: Iterable[Point | Sequence[float]], close: bool = True) -> list[float]:
    outline = normalize_points(points)
    if close:
        outline = close_outline(outline)
    return [distance(a, b) for a, b in zip(outline, outline[1:])]


def polygon_area(points: Iterable[Point | Sequence[float]]) -> float:
    outline = close_outline(points)
    if len(outline) < 4:
        return 0.0
    total = 0.0
    for a, b in zip(outline, outline[1:]):
        total += a.x * b.y - b.x * a.y
    return abs(total) / 2.0


def signed_area(points: Iterable[Point | Sequence[float]]) -> float:
    outline = close_outline(points)
    total = 0.0
    for a, b in zip(outline, outline[1:]):
        total += a.x * b.y - b.x * a.y
    return total / 2.0


def is_clockwise(points: Iterable[Point | Sequence[float]]) -> bool:
    return signed_area(points) < 0


def bounds(points: Iterable[Point | Sequence[float]]) -> tuple[float, float, float, float]:
    outline = normalize_points(points)
    if not outline:
        raise ValueError("at least one point is required")
    xs = [point.x for point in outline]
    ys = [point.y for point in outline]
    return min(xs), min(ys), max(xs), max(ys)


def point_in_polygon(point: Point | Sequence[float], polygon: Iterable[Point | Sequence[float]]) -> bool:
    p = as_point(point)
    outline = close_outline(polygon)
    if len(outline) < 4:
        return False

    inside = False
    for a, b in zip(outline, outline[1:]):
        if _point_on_segment(p, a, b):
            return True
        crosses = (a.y > p.y) != (b.y > p.y)
        if crosses:
            x_at_y = (b.x - a.x) * (p.y - a.y) / (b.y - a.y) + a.x
            if p.x < x_at_y:
                inside = not inside
    return inside


def _point_on_segment(p: Point, a: Point, b: Point, tolerance: float = 1e-9) -> bool:
    cross = (p.y - a.y) * (b.x - a.x) - (p.x - a.x) * (b.y - a.y)
    if not isclose(cross, 0.0, abs_tol=tolerance):
        return False
    return (
        min(a.x, b.x) - tolerance <= p.x <= max(a.x, b.x) + tolerance
        and min(a.y, b.y) - tolerance <= p.y <= max(a.y, b.y) + tolerance
    )
