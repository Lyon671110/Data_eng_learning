# Point Cloud Learning

点云处理学习模块，覆盖 KITTI 数据读取、可视化、滤波、配准与坐标系变换。

## 环境准备

需要 [Poetry](https://python-poetry.org/) 2.x。

```bash
cd point-cloud-learn
poetry install
```

> **WSL / 无显示器环境**：Open3D 交互窗口可能无法响应 Q/Esc。推荐加 `--no-viz`，改为离屏渲染保存 PNG：
>
> ```bash
> poetry run python examples/02_visualize_pointcloud.py --no-viz
> ```
>
> 或设置环境变量：`export OPEN3D_HEADLESS=1`

## 学习路线

| 编号 | 文件 | 主题 | 时长 | 实践任务 |
|------|------|------|------|----------|
| 01 | `examples/01_kitti_bin_read.py` | 点云数据结构 | 20 min | 用 numpy 读取 KITTI .bin，打印 shape 和前 5 个点 |
| 02 | `examples/02_visualize_pointcloud.py` | 3D 可视化基础 | 30 min | matplotlib / Open3D 绘制散点图 |
| 03 | `examples/03_open3d_basics.py` | Open3D 入门 | 20 min | 加载官方示例，旋转/缩放视图 |
| 04 | `examples/04_voxel_downsampling.py` | 体素下采样 | 30 min | 下采样并对比点数变化 |
| 05 | `examples/05_statistical_outlier_removal.py` | 统计去噪 SOR | 30 min | SOR 滤波，可视化前后效果 |
| 06 | `examples/06_radius_filter.py` | 半径滤波 | 20 min | 手写 + Open3D 半径滤波 |
| 07 | `examples/07_transform_matrix.py` | 变换矩阵 | 30 min | 手动应用旋转矩阵和平移向量 |
| 08 | `examples/08_icp_registration.py` | ICP 配准 | 30 min | Open3D ICP 对齐两帧点云 |
| 09 | `examples/09_coordinate_systems.py` | 坐标系与 TF 树 | 20 min | 绘制传感器安装位置示意图 |
| 10 | `examples/10_lidar_to_vehicle_frame.py` | 坐标系投影 | 30 min | 外参变换到车辆坐标系 |
| 11 | `examples/11_comprehensive_exercise.py` | 综合练习 | 90 min | 去噪→下采样→ICP→输出变换矩阵 |

## 快速运行

```bash
cd point-cloud-learn

# 在 Poetry 虚拟环境中运行
poetry run python examples/01_kitti_bin_read.py

# 或先进入 shell，再运行任意示例
poetry shell
python examples/01_kitti_bin_read.py
```

首次运行会自动在 `data/` 生成合成点云（无需下载 KITTI）。若使用真实 KITTI 数据，将 `.bin` 文件放入 `data/` 并修改脚本中的路径即可。

## 使用真实 KITTI 数据

1. 从 [KITTI Raw Data](https://www.cvlibs.net/datasets/kitti/raw_data.php) 下载序列
2. 点云位于 `velodyne_points/data/*.bin`
3. 标定文件位于 `calib_*.txt`

```python
# 替换示例中的路径
bin_path = "/path/to/kitti/2011_09_26/2011_09_26_drive_0001_sync/velodyne_points/data/0000000000.bin"
```

## 目录结构

```
point-cloud-learn/
├── README.md
├── pyproject.toml       # Poetry 依赖管理
├── poetry.lock          # 锁定版本（poetry install 后生成）
├── data/                # 自动生成的合成数据 / 放置 KITTI 数据
├── output/              # 脚本输出（图片、配准结果等）
├── utils/
│   ├── kitti_loader.py
│   └── sample_data.py
└── examples/
    ├── 01_kitti_bin_read.py
    ├── ...
    └── 11_comprehensive_exercise.py
```

## 核心概念速查

### KITTI .bin 格式

每个点 4 × `float32`：`[x, y, z, intensity]`，按行主序扁平存储。

### .pcd 格式常见字段

```
FIELDS x y z intensity ring timestamp
```

### 刚体变换

```
P' = R @ P + t        # 3×3 旋转 + 3×1 平移
T = [R | t]           # 4×4 齐次变换矩阵
    [0 | 1]
```

### ICP 配准

迭代最近点算法，最小化两帧点云对应点距离，需要较好初值。
