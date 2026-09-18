# Braidge Open Source

Reusable building blocks for stone fabrication and countertop fabrication software.

Stone shops are practical, precise, and often underserved by software. Many small
and mid-sized countertop fabricators still move between tape-measure fractions,
paper sketches, CAD files, spreadsheets, and manual translation before a drawing
is ready for the shop floor. This repository collects small, independent tools
that make those workflows easier to build around.

The goal is not to publish the Braidge production system. The goal is to share
low-level, industry-shaped utilities that other developers and fabrication shops
can reuse.

## What Is Included

- Inch fraction parsing, formatting, arithmetic, and 1/16 inch snapping.
- Basic 2D countertop geometry helpers for rectangles, clipped corners,
  polygon area, bounds, closure checks, and edge lengths.
- Generic cutout validation for sinks, cooktops, grommets, and custom openings.
- Lightweight DXF helpers for simple outlines, rectangular cutouts, circular
  holes, labels, and generic shop layers.
- Tests, examples, and documentation for the public API.

## What Is Not Included

This repository intentionally excludes Braidge commercial code and operational
logic, including:

- Proprietary production orchestration and commercial workflow automation.
- Private production rules and machine-integration logic.
- Customer, tenant, billing, deployment, and private runbook logic.
- Real production cases, drawings, internal prompts, secrets, and private
  validation data.

There is no automatic sync from private Braidge repositories into this one.
Every public release should be selected manually, reviewed, sanitized, tested,
and approved.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Quick Example

```python
from braidge_tools.fractions import parse_inches, format_inches
from braidge_tools.geometry import rectangle, polygon_area
from braidge_tools.cutouts import Cutout, validate_cutouts

width = parse_inches("96 1/2")
depth = parse_inches("25 1/2")

outline = rectangle(float(width), float(depth))
sink = Cutout(kind="sink", x=48.0, y=12.75, width=30.0, height=16.0)

print(format_inches(width + depth))
print(polygon_area(outline))
print(validate_cutouts(outline, [sink], min_edge_clearance=3.0))
```

> Clearance values in examples are illustrative and configurable. They are not
> a substitute for material-, equipment-, or shop-specific fabrication requirements.

## Generate A Simple DXF

```bash
python examples/simple_countertop.py
```

The example writes `examples/output/simple_countertop.dxf`.

## Repository Layout

```text
src/braidge_tools/
  fractions.py      # inch fraction utilities
  geometry.py       # small 2D geometry helpers
  cutouts.py        # generic opening validation
  dxf.py            # lightweight ezdxf helpers

tests/              # pytest coverage
examples/           # runnable examples
docs/               # release gate and industry notes
```

## Release Rule

Before making this repository public or publishing a release, follow
[`docs/oss-release-gate.md`](docs/oss-release-gate.md).
