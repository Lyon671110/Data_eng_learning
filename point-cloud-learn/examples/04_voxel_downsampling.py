"""
04 体素下采样（Voxel Downsampling）原理
实践任务：对点云执行下采样，对比点数变化并可视化
预计时长：30 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin
from utils.sample_data import ensure_sample_data
from utils.visualize import show_geometries

# ---------------------------------------------------------------------------
# 体素下采样原理:
#   1. 将 3D 空间划分为边长为 voxel_size 的立方体网格
#   2. 每个体素内的所有点合并为一个代表点（通常取质心）
#   3. 有效降低点数，同时保持整体几何形状
# ---------------------------------------------------------------------------


def voxel_downsample_manual(points: np.ndarray, voxel_size: float) -> np.ndarray:
    """手写体素下采样（帮助理解原理）。"""
    xyz = points[:, :3]
    # 将坐标量化到体素索引
    voxel_idx = np.floor(xyz / voxel_size).astype(np.int64)
    # 用字典聚合每个体素内的点
    voxels: dict[tuple, list] = {}
    for i, key in enumerate(map(tuple, voxel_idx)):
        voxels.setdefault(key, []).append(i)

    centroids = []
    for indices in voxels.values():
        centroids.append(xyz[indices].mean(axis=0))
    return np.array(centroids)


def main():
    import open3d as o3d

    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)
    points = read_kitti_bin(paths["frame_00"])
    pcd = points_to_open3d(points)

    voxel_sizes = [0.05, 0.1, 0.2, 0.5]
    print("=== 体素下采样对比 ===")
    print(f"{'voxel_size':>12}  {'点数':>8}  {'压缩比':>8}")
    print("-" * 34)
    original_n = len(pcd.points)
    downsampled_pcds = []

    for vs in voxel_sizes:
        ds = pcd.voxel_down_sample(voxel_size=vs)
        ratio = original_n / len(ds.points)
        print(f"{vs:12.2f}  {len(ds.points):8d}  {ratio:7.1f}x")
        ds.paint_uniform_color([0.1 + vs, 0.5, 0.8 - vs])
        downsampled_pcds.append(ds)

    # 手写实现对比
    manual = voxel_downsample_manual(points, voxel_size=0.2)
    o3d_manual = o3d.geometry.PointCloud()
    o3d_manual.points = o3d.utility.Vector3dVector(manual)
    print(f"\n手写实现 (voxel=0.2): {len(manual)} 点")
    print(f"Open3D 实现 (voxel=0.2): {len(pcd.voxel_down_sample(0.2).points)} 点")

    # 可视化：原始 vs 下采样
    pcd.paint_uniform_color([0.7, 0.7, 0.7])
    best_ds = pcd.voxel_down_sample(voxel_size=0.2)
    best_ds.paint_uniform_color([1.0, 0.3, 0.1])
    print("\n灰色=原始, 红色=下采样(voxel=0.2)")
    show_geometries(
        [pcd, best_ds],
        window_name="体素下采样对比",
        output_path=Path(__file__).parent.parent / "output" / "04_voxel_downsample.png",
    )


if __name__ == "__main__":
    main()
