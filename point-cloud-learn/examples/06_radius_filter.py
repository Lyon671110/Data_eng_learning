"""
06 半径滤波简介
实践任务：实现简单的半径滤波（可手写或调库）
预计时长：20 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin
from utils.sample_data import ensure_sample_data
from utils.visualize import show_geometries

# ---------------------------------------------------------------------------
# 半径滤波 (Radius Outlier Removal) 原理:
#   对每个点，统计半径 r 内的邻居数量
#   若邻居数 < min_neighbors，则判定为孤立噪点并剔除
#   适合去除稀疏飞点，与 SOR 互补
# ---------------------------------------------------------------------------


def radius_filter_manual(
    points: np.ndarray,
    radius: float,
    min_neighbors: int,
) -> np.ndarray:
    """手写半径滤波（暴力实现，仅用于学习，大点云请用 Open3D）。"""
    xyz = points[:, :3]
    n = len(xyz)
    keep = np.zeros(n, dtype=bool)

    for i in range(n):
        dists = np.linalg.norm(xyz - xyz[i], axis=1)
        count = (dists < radius).sum() - 1  # 排除自身
        keep[i] = count >= min_neighbors

    return keep


def main():
    import open3d as o3d

    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)
    points = read_kitti_bin(paths["noisy"])
    pcd = points_to_open3d(points)

    radius = 0.5
    min_neighbors = 8

    print(f"滤波前点数: {len(pcd.points)}")
    print(f"参数: radius={radius}m, min_neighbors={min_neighbors}")

    # Open3D 库实现
    pcd_clean, inlier_mask = pcd.remove_radius_outlier(
        nb_points=min_neighbors,
        radius=radius,
    )
    inlier_mask = np.array(inlier_mask)
    print(f"Open3D 滤波后: {len(pcd_clean.points)} 点, 剔除 {(~inlier_mask).sum()} 个")

    # 手写实现（采样验证，全量太慢）
    sample_n = min(500, len(points))
    idx = np.random.choice(len(points), sample_n, replace=False)
    manual_mask = radius_filter_manual(points[idx], radius, min_neighbors)
    print(f"手写实现（{sample_n} 点采样验证）: 保留 {manual_mask.sum()} 点")

    pcd_inlier = pcd.select_by_index(np.where(inlier_mask)[0])
    pcd_outlier = pcd.select_by_index(np.where(~inlier_mask)[0])
    pcd_inlier.paint_uniform_color([0.2, 0.7, 0.3])
    pcd_outlier.paint_uniform_color([1.0, 0.2, 0.2])

    print("\n绿色=保留, 红色=半径滤波剔除")
    show_geometries(
        [pcd_inlier, pcd_outlier],
        window_name="半径滤波效果",
        output_path=Path(__file__).parent.parent / "output" / "06_radius_filter.png",
    )


if __name__ == "__main__":
    main()
