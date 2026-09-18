# Stone Fabrication Software Notes

Countertop fabrication often combines precise craft with fragmented digital
tools. A shop may receive a hand sketch, verify dimensions with a tape measure,
enter quantities in a spreadsheet, clean geometry in CAD, and then prepare a
machine-readable drawing.

Public, reusable software should help with the repeatable pieces:

- Exact inch fractions, because shop measurements are often written as fractions
  rather than decimals.
- Small geometry primitives, because many countertop parts start as rectangles,
  L-shapes, clipped corners, arcs, holes, and simple edge annotations.
- DXF helpers, because DXF remains a practical interchange format between
  lightweight software, CAD, saws, routers, and waterjets.
- Cutout checks, because sinks, cooktops, faucets, grommets, and custom openings
  need basic size and clearance validation before production review.

The public toolkit should stay at this foundation layer. Shop-specific
automation, commercial production policy, and customer workflow belong in
private systems.
