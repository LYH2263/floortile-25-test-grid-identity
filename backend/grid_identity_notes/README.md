# 网格乘积恒等测例说明

本目录为**网格乘积恒等测例**的配套说明，只描述行列网格（cols/rows/grid_count）的
恒等校验，不涉及损耗系数与开洞/洞口类旧逻辑，故目录与文件名均避开这些旧称。

## 入口模块名

- 被测入口模块：`app.engines.tile_math`
  - `layout_preview(room_l, room_w, tile_l, tile_w)`：返回 `cols`、`rows`、`grid_count`
  - `tile_count(room_l, room_w, tile_l, tile_w, waste_pct)`：面积法 `raw_count`，并内嵌同输入的 `layout`
- 测例文件：`app/tests/test_grid_product_identity.py`（独立文件，pytest 自动收集）
- 收集与运行（在 `backend/` 目录下）：

  ```bash
  python -m pytest app/tests/test_grid_product_identity.py -v
  python -m pytest app/tests/test_grid_product_identity.py -v -s   # 同时打印每行长宽砖边与算得行列
  ```

- 旧有客餐厅片数断言文件 `app/tests/test_tile_math.py` 原样保留，未改动。

## 恒等与校验要点

1. **乘积恒等**：对每行夹具断言 `layout.cols * layout.rows == layout.grid_count`。
2. **网格法对面积法**：同一组输入再经 `tile_count(..., waste_pct=0.0)` 取面积法
   `raw_count`，断言 `grid_count >= raw_count`（由 ⌈L/a⌉·⌈W/b⌉ ≥ ⌈LW/(ab)⌉ 恒成立）。
   其中客餐厅种子为显式样板：`80 >= 75`。
3. **参数拒绝**：砖边为零或负数时 `layout_preview` 抛 `ValueError`（消息含“非正砖边”）。
4. **失败消息可区分**：
   - 乘积/期望值类失败前缀为 `[乘积恒等失败]`（含 `[乘积恒等失败-网格不少于面积法]`）；
   - 参数未被拒绝或异常消息不符前缀为 `[参数拒绝失败]`。
   两类消息均打印该行夹具的房长、房宽、砖长、砖宽与算得的 cols/rows。

## 夹具表

### 网格恒等夹具（5 组：2 组种子 + 3 组手写几何）

| 夹具编号 | 来源 | 房长 L | 房宽 W | 砖长 a | 砖宽 b | cols | rows | grid_count | 面积法 raw_count |
|---|---|---|---|---|---|---|---|---|---|
| `seed_living_dining` | 客餐厅种子（seed.py：客餐厅 6.0×4.5 + 600×600 砖） | 6.0 | 4.5 | 0.6 | 0.6 | 10 | 8 | 80 | 75 |
| `seed_corridor` | 狭长走廊种子（seed.py：狭长走廊 8.0×1.2 + 800×800 砖） | 8.0 | 1.2 | 0.8 | 0.8 | 10 | 2 | 20 | 15 |
| `geo_square_cut` | 手写几何 1：小方房双向切边 | 2.5 | 2.0 | 0.6 | 0.6 | 5 | 4 | 20 | 14 |
| `geo_exact_tile` | 手写几何 2：整数整除基准 | 3.0 | 3.0 | 1.0 | 1.0 | 3 | 3 | 9 | 9 |
| `geo_rect_tile` | 手写几何 3：长方砖横铺窄房 | 4.2 | 1.5 | 0.7 | 0.3 | 6 | 5 | 30 | 30 |

每组均断言：`cols`、`rows` 等于表中期望值，且 `cols * rows == grid_count`，
并在同输入的面积法结果上断言 `grid_count >= raw_count`。

### 非正砖边拒绝夹具（3 组）

| 夹具编号 | 房长 L | 房宽 W | 砖长 a | 砖宽 b | 说明 |
|---|---|---|---|---|---|
| `reject_zero_l` | 3.0 | 3.0 | 0.0 | 0.6 | 砖长为零 |
| `reject_neg_w` | 3.0 | 3.0 | 0.6 | -0.8 | 砖宽为负 |
| `reject_both_neg` | 3.0 | 3.0 | -0.6 | -0.6 | 双砖边均负 |

每组均断言抛出 `ValueError` 且异常消息包含“非正砖边”。
