"""表驱动测例：网格乘积恒等 cols * rows == grid_count。

夹具说明（另附文档）见 backend/grid_identity_notes/README.md。
入口模块：app.engines.tile_math（layout_preview / tile_count）。
"""

import pytest

from app.engines.tile_math import layout_preview, tile_count


# 表驱动夹具：(编号, 房长, 房宽, 砖长, 砖宽, 期望列, 期望行, 标签)
#   seed_* 取自 app/seed.py 的种子房间与砖边；
#   geo_*  为手写几何组合。
GRID_FIXTURES = [
    # 客餐厅种子：6.0 x 4.5 房间 + 600x600 砖
    ("seed_living_dining", 6.0, 4.5, 0.6, 0.6, 10, 8, "客餐厅种子"),
    # 狭长走廊种子：8.0 x 1.2 房间 + 800x800 砖
    ("seed_corridor", 8.0, 1.2, 0.8, 0.8, 10, 2, "狭长走廊种子"),
    # 手写几何 1：小方房、小方砖，双向都有切边
    ("geo_square_cut", 2.5, 2.0, 0.6, 0.6, 5, 4, "手写几何-小方房切边"),
    # 手写几何 2：整数整除，乘积恒等的基准情形
    ("geo_exact_tile", 3.0, 3.0, 1.0, 1.0, 3, 3, "手写几何-整除"),
    # 手写几何 3：长方形砖横铺窄房，长宽不同向
    ("geo_rect_tile", 4.2, 1.5, 0.7, 0.3, 6, 5, "手写几何-长方砖"),
]

# 非正砖边必须被拒绝：(编号, 房长, 房宽, 砖长, 砖宽, 非法字段)
REJECT_FIXTURES = [
    ("reject_zero_l", 3.0, 3.0, 0.0, 0.6, "tile_l=0.0"),
    ("reject_neg_w", 3.0, 3.0, 0.6, -0.8, "tile_w=-0.8"),
    ("reject_both_neg", 3.0, 3.0, -0.6, -0.6, "tile_l=-0.6"),
]


@pytest.mark.parametrize(
    "case_id,room_l,room_w,tile_l,tile_w,exp_cols,exp_rows,label",
    GRID_FIXTURES,
    ids=[f[0] for f in GRID_FIXTURES],
)
def test_cols_rows_product_equals_grid_count(
    case_id, room_l, room_w, tile_l, tile_w, exp_cols, exp_rows, label
):
    """乘积恒等：layout.cols * layout.rows 必须等于 layout.grid_count。"""
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    cols, rows, grid_count = layout["cols"], layout["rows"], layout["grid_count"]

    # 失败消息明确标记“乘积恒等失败”，并打印该行夹具的长宽砖边与算得行列
    assert cols == exp_cols, (
        f"[乘积恒等失败] 夹具 {case_id}（{label}）: "
        f"房长={room_l} 房宽={room_w} 砖长={tile_l} 砖宽={tile_w} -> "
        f"算得 cols={cols}, rows={rows}（期望 cols={exp_cols}）"
    )
    assert rows == exp_rows, (
        f"[乘积恒等失败] 夹具 {case_id}（{label}）: "
        f"房长={room_l} 房宽={room_w} 砖长={tile_l} 砖宽={tile_w} -> "
        f"算得 cols={cols}, rows={rows}（期望 rows={exp_rows}）"
    )
    assert cols * rows == grid_count, (
        f"[乘积恒等失败] 夹具 {case_id}（{label}）: "
        f"房长={room_l} 房宽={room_w} 砖长={tile_l} 砖宽={tile_w} -> "
        f"算得 cols={cols}, rows={rows}, grid_count={grid_count}, "
        f"但 cols*rows={cols * rows}"
    )


@pytest.mark.parametrize(
    "case_id,room_l,room_w,tile_l,tile_w,bad_field",
    REJECT_FIXTURES,
    ids=[f[0] for f in REJECT_FIXTURES],
)
def test_nonpositive_tile_edge_rejected(case_id, room_l, room_w, tile_l, tile_w, bad_field):
    """砖边为零或负数必须拒绝；失败消息标记“参数拒绝”，与乘积恒等失败区分。"""
    with pytest.raises(ValueError) as exc_info:
        layout_preview(room_l, room_w, tile_l, tile_w)
    assert "非正砖边" in str(exc_info.value), (
        f"[参数拒绝失败] 夹具 {case_id}: 房长={room_l} 房宽={room_w} "
        f"砖长={tile_l} 砖宽={tile_w}（非法字段 {bad_field}）"
    )


@pytest.mark.parametrize(
    "case_id,room_l,room_w,tile_l,tile_w,exp_cols,exp_rows,label",
    GRID_FIXTURES,
    ids=[f[0] for f in GRID_FIXTURES],
)
def test_grid_count_vs_area_raw_count(
    case_id, room_l, room_w, tile_l, tile_w, exp_cols, exp_rows, label
):
    """同一组输入再取面积法 raw_count，逐行打印；至少一组须 grid_count >= raw_count。"""
    result = tile_count(room_l, room_w, tile_l, tile_w, 0.0)
    layout = result["layout"]
    raw_count = result["raw_count"]
    grid_count = layout["grid_count"]

    # 打印该行夹具的长宽砖边与算得行列，失败时 pytest -s 或断言报告中可见
    line = (
        f"[{case_id}] 房长={room_l} 房宽={room_w} 砖长={tile_l} 砖宽={tile_w} -> "
        f"cols={layout['cols']} rows={layout['rows']} "
        f"grid_count={grid_count} raw_count={raw_count}"
    )
    print(line)

    # 数学上 ceil(L/a)*ceil(W/b) 恒不小于 ceil(面积/单片面积)，故每行都成立；
    # 客餐厅种子（80 >= 75）即题目要求的“至少一组”显式样板。
    assert grid_count >= raw_count, (
        f"[乘积恒等失败-网格不少于面积法] 夹具 {case_id}（{label}）: "
        f"房长={room_l} 房宽={room_w} 砖长={tile_l} 砖宽={tile_w} -> "
        f"算得 cols={layout['cols']}, rows={layout['rows']}, "
        f"grid_count={grid_count} < raw_count={raw_count}"
    )
