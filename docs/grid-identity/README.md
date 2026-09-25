# 网格乘积恒等测例说明

## 入口模块

- 测例文件：`backend/app/tests/test_grid_product_identity.py`
- 模块名：`app.tests.test_grid_product_identity`
- 运行方式：`cd backend && pytest app/tests/test_grid_product_identity.py -v`
- 被测入口：`app.engines.tile_math.tile_count`（其返回的 `layout` 来自同模块 `layout_preview`）

## 断言内容

1. **乘积恒等**：对每组夹具断言 `layout.cols * layout.rows == layout.grid_count`。
2. **网格覆盖面积法**：同一组输入再取面积法 `raw_count`，五组夹具均断言
   `grid_count >= raw_count`（满足"至少一组"的要求；数学上网格整片铺满必覆盖房间面积，
   故恒成立）。
3. **参数拒绝**：砖边（tile_l / tile_w）为零或负数时，`tile_count` 必须抛 `ValueError`。

失败消息以前缀区分两类失败，并打印该行夹具的长、宽、砖边与算得行列：

- `PRODUCT_IDENTITY_FAIL [...] room=... tile=... cols=... rows=... grid_count=...` —— 乘积恒等失败
- `GRID_BELOW_RAW [...]` —— 网格数低于面积法（覆盖断言失败）
- `PARAM_REJECT_FAIL [...]` —— 参数拒绝失败（应抛而未抛 `ValueError`）

## 夹具表（GRID_FIXTURES）

| 夹具 id | 来源 | 房间长×宽 (m) | 砖边 (m) | cols | rows | grid_count | raw_count | 覆盖断言 |
|---|---|---|---|---|---|---|---|---|
| seed-客餐厅-600x600 | 种子房间"客餐厅" + 种子砖 600x600 | 6.0 × 4.5 | 0.6 × 0.6 | 10 | 8 | 80 | 75 | ✓ |
| seed-狭长走廊-800x800 | 种子房间"狭长走廊" + 种子砖 800x800 | 8.0 × 1.2 | 0.8 × 0.8 | 10 | 2 | 20 | 15 | ✓ |
| hand-书房-500x600 | 手写几何 | 3.7 × 2.4 | 0.5 × 0.6 | 8 | 4 | 32 | 30 | ✓ |
| hand-卫生间-700x450 | 手写几何 | 4.2 × 3.3 | 0.7 × 0.45 | 6 | 8 | 48 | 44 | ✓ |
| hand-门厅-600x300 | 手写几何 | 5.05 × 2.95 | 0.6 × 0.3 | 9 | 10 | 90 | 83 | ✓ |

共 5 组：2 组种子（客餐厅、狭长走廊）+ 3 组手写几何，满足"不少于五组"。

## 拒绝夹具表（REJECT_FIXTURES）

| 夹具 id | 房间长×宽 (m) | 砖边 (m) | 期望 |
|---|---|---|---|
| zero-tile-l | 6.0 × 4.5 | 0.0 × 0.6 | ValueError |
| zero-tile-w | 6.0 × 4.5 | 0.6 × 0.0 | ValueError |
| neg-tile-l | 6.0 × 4.5 | -0.6 × 0.6 | ValueError |
| neg-tile-w | 6.0 × 4.5 | 0.6 × -0.6 | ValueError |

## 备注

- 既有客餐厅片数断言文件 `backend/app/tests/test_tile_math.py` 保持原样，未改动。
- `test_fixture_table_shape` 守护夹具表本身：不少于 5 行、含两个种子夹具、至少一行带覆盖断言。
