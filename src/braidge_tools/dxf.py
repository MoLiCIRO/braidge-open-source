"""Lightweight DXF helpers for examples and simple shop drawings."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import ezdxf

from braidge_tools.cutouts import Cutout
from braidge_tools.geometry import Point, close_outline, normalize_points

OUTLINE_LAYER = "BRAIDGE_OUTLINE"
CUTOUT_LAYER = "BRAIDGE_CUTOUT"
TEXT_LAYER = "BRAIDGE_TEXT"


def new_document():
    doc = ezdxf.new("R2010", setup=True)
    _ensure_layer(doc, OUTLINE_LAYER, color=7)
    _ensure_layer(doc, CUTOUT_LAYER, color=3)
    _ensure_layer(doc, TEXT_LAYER, color=2)
    return doc


def add_outline(modelspace, points: Iterable[Point | tuple[float, float]], *, layer: str = OUTLINE_LAYER):
    outline = close_outline(points)
    modelspace.add_lwpolyline([(point.x, point.y) for point in outline], close=True, dxfattribs={"layer": layer})


def add_cutout(modelspace, cutout: Cutout, *, layer: str = CUTOUT_LAYER):
    if cutout.is_round:
        modelspace.add_circle((cutout.x, cutout.y), cutout.radius, dxfattribs={"layer": layer})
        return

    x1 = cutout.x - cutout.half_width
    x2 = cutout.x + cutout.half_width
    y1 = cutout.y - cutout.half_height
    y2 = cutout.y + cutout.half_height
    add_outline(modelspace, [Point(x1, y1), Point(x2, y1), Point(x2, y2), Point(x1, y2)], layer=layer)


def add_label(modelspace, text: str, at: Point | tuple[float, float], *, height: float = 2.0):
    point = normalize_points([at])[0]
    modelspace.add_text(text, dxfattribs={"layer": TEXT_LAYER, "height": height}).set_placement((point.x, point.y))


def write_simple_countertop_dxf(
    path: str | Path,
    outline: Iterable[Point | tuple[float, float]],
    cutouts: Iterable[Cutout] = (),
    *,
    label: str | None = None,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = new_document()
    modelspace = doc.modelspace()
    add_outline(modelspace, outline)
    for cutout in cutouts:
        add_cutout(modelspace, cutout)
        if cutout.label:
            add_label(modelspace, cutout.label, (cutout.x + cutout.half_width + 1.0, cutout.y))
    if label:
        add_label(modelspace, label, (0, -4))
    doc.saveas(target)
    return target


def _ensure_layer(doc, name: str, *, color: int):
    if name not in doc.layers:
        doc.layers.add(name, color=color)
