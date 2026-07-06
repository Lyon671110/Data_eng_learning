"""
05 统计去噪（Statistical Outlier Removal, SOR）
实践任务：加载含噪点云，用 SOR 滤波，可视化去噪前后效果
预计时长：30 min
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin
from utils.sample_data import ensure_sample_data

# ---------------------------------------------------------------------------
# SOR 原理:
#   1. 对每个点，计算其到 k 个最近邻的平均距离 d
#   2. 假设所有 d 服从高斯分布，计算全局均值 μ 和标准差 σ
#   3. 若 d > μ + std_ratio × σ，则判定为离群点并剔除
# ---------------------------------------------------------------------------


def main():
    import open3d as o3d
    import numpy as np

    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)
    points = read_kitti_bin(paths["noisy"])
    pcd = points_to_open3d(points)

    print(f"去噪前点数: {len(pcd.points)}")

    nb_neighbors = 20   # k 近邻数量
    std_ratio = 2.0     # 标准差倍数阈值

    pcd_clean, inlier_mask = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio,
    )
    inlier_mask = np.array(inlier_mask)
    n_removed = (~inlier_mask).sum()

    print(f"去噪后点数: {len(pcd_clean.points)}")
    print(f"剔除离群点: {n_removed} 个 ({100 * n_removed / len(pcd.points):.1f}%)")
    print(f"参数: nb_neighbors={nb_neighbors}, std_ratio={std_ratio}")

    # 可视化：红色=离群点，灰色=内点
    pcd_inlier = pcd.select_by_index(np.where(inlier_mask)[0])
    pcd_outlier = pcd.select_by_index(np.where(~inlier_mask)[0])
    pcd_inlier.paint_uniform_color([0.6, 0.6, 0.6])
    pcd_outlier.paint_uniform_color([1.0, 0.1, 0.1])

    print("\n灰色=内点, 红色=被剔除的离群点")
    o3d.visualization.draw_geometries(
        [pcd_inlier, pcd_outlier],
        window_name="SOR 统计去噪前后对比",
    )


if __name__ == "__main__":
    main()
