from braidge_tools.geometry import Point, bounds, clipped_rectangle, edge_lengths, is_closed, point_in_polygon, polygon_area, rectangle


def test_rectangle_geometry():
    outline = rectangle(10, 5)
    assert polygon_area(outline) == 50
    assert bounds(outline) == (0, 0, 10, 5)
    assert edge_lengths(outline) == [10, 5, 10, 5]


def test_clipped_rectangle():
    outline = clipped_rectangle(10, 5, clip=2, corner="top-right")
    assert len(outline) == 5
    assert polygon_area(outline) == 48


def test_point_in_polygon_includes_boundary():
    outline = rectangle(10, 5)
    assert point_in_polygon(Point(4, 2), outline)
    assert point_in_polygon(Point(0, 2), outline)
    assert not point_in_polygon(Point(11, 2), outline)


def test_is_closed():
    assert is_closed([(0, 0), (1, 0), (0, 0)])
    assert not is_closed([(0, 0), (1, 0)])
