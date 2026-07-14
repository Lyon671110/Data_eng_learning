"""
01 点云数据结构：xyz、intensity、ring 等字段；.bin/.pcd 格式说明
实践任务：用 numpy 读取 KITTI .bin，打印 shape 和前 5 个点
预计时长：20 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.sample_data import ensure_sample_data

# ---------------------------------------------------------------------------
# 点云字段说明
# ---------------------------------------------------------------------------
# KITTI Velodyne .bin:
#   - 每个点 4 × float32: [x, y, z, intensity]
#   - x, y, z: 激光雷达坐标系下的米制坐标
#   - intensity: 反射强度（0~1 或设备相关范围）
#
# .pcd (Point Cloud Data) 常见字段:
#   - FIELDS x y z intensity ring timestamp
#   - x/y/z: 坐标
#   - intensity: 反射强度
#   - ring: 激光线束编号（多线雷达）
#   - timestamp: 每个点的采集时间（部分设备）
# ---------------------------------------------------------------------------


def main():
    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)

    # 如有真实 KITTI 数据，可替换路径，例如:
    # bin_path = "path/to/velodyne/000000.bin"
    bin_path = paths["frame_00"]
    print(f"读取文件: {bin_path}")

    # --- 用 numpy 读取 KITTI .bin ---
    # 1. np.fromfile: 按 float32 逐字节读取整个二进制文件，得到一维数组
    raw = np.fromfile(bin_path, dtype=np.float32)
    # 2. reshape: 每 4 个值组成一个点 [x, y, z, intensity]
    points = raw.reshape(-1, 4)

    print("\n=== 基本信息 ===")
    print(f"dtype : {points.dtype}")
    print(f"shape : {points.shape}  → (点数, 4)  列依次为 x, y, z, intensity")

    print("\n=== 前 5 个点 ===")
    header = f"{'idx':>4}  {'x':>10}  {'y':>10}  {'z':>10}  {'intensity':>10}"
    print(header)
    print("-" * len(header))
    for i, pt in enumerate(points[:5]):
        print(f"{i:4d}  {pt[0]:10.3f}  {pt[1]:10.3f}  {pt[2]:10.3f}  {pt[3]:10.3f}")
    print(points[points[:,2]>2])
    print("\n=== 各字段统计 ===")
    for col, name in enumerate(["x", "y", "z", "intensity"]):
        col_data = points[:, col]
        print(f"  {name:10s}: min={col_data.min():8.3f}  max={col_data.max():8.3f}  mean={col_data.mean():8.3f}")


if __name__ == "__main__":
    main()
