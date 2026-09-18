from pathlib import Path

from braidge_tools.cutouts import Cutout
from braidge_tools.dxf import write_simple_countertop_dxf
from braidge_tools.geometry import rectangle


def test_write_simple_countertop_dxf(tmp_path: Path):
    output = write_simple_countertop_dxf(
        tmp_path / "simple.dxf",
        rectangle(40, 20),
        [Cutout(kind="faucet", x=20, y=10, width=2)],
        label="Test",
    )
    assert output.exists()
    assert output.read_text(encoding="utf-8", errors="ignore").startswith("  0")
