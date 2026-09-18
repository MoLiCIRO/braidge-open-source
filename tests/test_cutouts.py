from braidge_tools.cutouts import Cutout, Severity, cutout_gap, validate_cutouts
from braidge_tools.geometry import rectangle


def test_valid_cutout_has_no_issues():
    outline = rectangle(96, 26)
    cutouts = [Cutout(kind="sink", x=48, y=13, width=30, height=16)]
    assert validate_cutouts(outline, cutouts, min_edge_clearance=3) == []


def test_cutout_outside_outline_is_error():
    outline = rectangle(30, 20)
    cutouts = [Cutout(kind="sink", x=28, y=10, width=10, height=10)]
    issues = validate_cutouts(outline, cutouts)
    assert any(issue.severity == Severity.ERROR and issue.code == "outside-outline" for issue in issues)


def test_edge_clearance_warning():
    outline = rectangle(30, 20)
    cutouts = [Cutout(kind="sink", x=15, y=3, width=10, height=4)]
    issues = validate_cutouts(outline, cutouts, min_edge_clearance=3)
    assert any(issue.code == "edge-clearance" for issue in issues)


def test_cutout_gap():
    left = Cutout(kind="sink", x=10, y=10, width=4, height=4)
    right = Cutout(kind="cooktop", x=20, y=10, width=4, height=4)
    assert cutout_gap(left, right) == 6
