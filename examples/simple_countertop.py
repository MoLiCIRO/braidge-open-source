from braidge_tools.cutouts import Cutout, validate_cutouts
from braidge_tools.dxf import write_simple_countertop_dxf
from braidge_tools.fractions import parse_inches
from braidge_tools.geometry import rectangle


def main() -> None:
    width = float(parse_inches("96 1/2"))
    depth = float(parse_inches("25 1/2"))
    outline = rectangle(width, depth)
    cutouts = [
        Cutout(kind="sink", x=48.0, y=12.75, width=30.0, height=16.0, label="Sink 30 x 16"),
        Cutout(kind="faucet", x=48.0, y=22.0, width=1.375, label="Faucet"),
    ]

    issues = validate_cutouts(outline, cutouts, min_edge_clearance=3.0)
    for issue in issues:
        print(f"{issue.severity.value}: {issue.code}: {issue.message}")

    output = write_simple_countertop_dxf(
        "examples/output/simple_countertop.dxf",
        outline,
        cutouts,
        label="Public example: simple countertop",
    )
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
