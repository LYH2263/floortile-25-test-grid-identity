"""Grid product identity: layout.cols * layout.rows == layout.grid_count.

Table-driven fixtures mix the seeded rooms (客餐厅, 狭长走廊) with
hand-written geometries. Failure messages carry distinct prefixes so a
product-identity break (PRODUCT_IDENTITY_FAIL) can be told apart from a
parameter-rejection break (PARAM_REJECT_FAIL) at a glance; each message
repeats the fixture row's room length/width, tile edges and the computed
cols/rows.

See docs/grid-identity/README.md for the fixture table.
"""

import pytest

from app.engines.tile_math import tile_count

# (id, room_l, room_w, tile_l, tile_w, waste_pct, assert grid_count >= raw_count)
GRID_FIXTURES = [
    ("seed-客餐厅-600x600", 6.0, 4.5, 0.6, 0.6, 8.0, True),
    ("seed-狭长走廊-800x800", 8.0, 1.2, 0.8, 0.8, 8.0, True),
    ("hand-书房-500x600", 3.7, 2.4, 0.5, 0.6, 8.0, True),
    ("hand-卫生间-700x450", 4.2, 3.3, 0.7, 0.45, 8.0, True),
    ("hand-门厅-600x300", 5.05, 2.95, 0.6, 0.3, 8.0, True),
]

# (id, room_l, room_w, tile_l, tile_w) — non-positive tile edge must be rejected
REJECT_FIXTURES = [
    ("zero-tile-l", 6.0, 4.5, 0.0, 0.6),
    ("zero-tile-w", 6.0, 4.5, 0.6, 0.0),
    ("neg-tile-l", 6.0, 4.5, -0.6, 0.6),
    ("neg-tile-w", 6.0, 4.5, 0.6, -0.6),
]


@pytest.mark.parametrize(
    "name,room_l,room_w,tile_l,tile_w,waste_pct,check_cover",
    GRID_FIXTURES,
    ids=[row[0] for row in GRID_FIXTURES],
)
def test_grid_product_identity(name, room_l, room_w, tile_l, tile_w, waste_pct, check_cover):
    r = tile_count(room_l, room_w, tile_l, tile_w, waste_pct)
    layout = r["layout"]
    cols, rows, grid = layout["cols"], layout["rows"], layout["grid_count"]
    assert cols * rows == grid, (
        f"PRODUCT_IDENTITY_FAIL [{name}] "
        f"room={room_l}x{room_w}m tile={tile_l}x{tile_w}m "
        f"cols={cols} rows={rows} grid_count={grid} cols*rows={cols * rows}"
    )
    if check_cover:
        assert grid >= r["raw_count"], (
            f"GRID_BELOW_RAW [{name}] "
            f"room={room_l}x{room_w}m tile={tile_l}x{tile_w}m "
            f"cols={cols} rows={rows} grid_count={grid} raw_count={r['raw_count']}"
        )


@pytest.mark.parametrize(
    "name,room_l,room_w,tile_l,tile_w",
    REJECT_FIXTURES,
    ids=[row[0] for row in REJECT_FIXTURES],
)
def test_non_positive_tile_edge_rejected(name, room_l, room_w, tile_l, tile_w):
    try:
        tile_count(room_l, room_w, tile_l, tile_w, 8.0)
    except ValueError:
        return  # rejected as required
    pytest.fail(
        f"PARAM_REJECT_FAIL [{name}] "
        f"room={room_l}x{room_w}m tile={tile_l}x{tile_w}m "
        f"expected ValueError for non-positive tile edge, none raised"
    )


def test_fixture_table_shape():
    """Guard the fixture requirements themselves."""
    assert len(GRID_FIXTURES) >= 5, "need at least five room/tile fixture rows"
    names = [row[0] for row in GRID_FIXTURES]
    assert any("客餐厅" in n for n in names), "missing 客餐厅 seed fixture"
    assert any("狭长走廊" in n for n in names), "missing 狭长走廊 seed fixture"
    assert any(row[6] for row in GRID_FIXTURES), (
        "need at least one row asserting grid_count >= raw_count"
    )
