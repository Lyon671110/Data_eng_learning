"""
08 ICP 配准原理与代码调用
实践任务：用 Open3D 的 ICP 对齐两帧稍有不同的点云
预计时长：30 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin
from utils.sample_data import ensure_sample_data

# ---------------------------------------------------------------------------
# ICP (Iterative Closest Point) 原理:
#   1. 给定源点云 source 和目标点云 target（位姿未知）
#   2. 迭代: 为 source 中每个点找 target 中最近点 → 计算最优 R,t 最小化距离
#   3. 将 R,t 应用到 source，重复直到收敛
# 前提: 两帧已有较好初值（相差不大），否则可能陷入局部最优
# ---------------------------------------------------------------------------


def main():
    import open3d as o3d

    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)

    source_pts = read_kitti_bin(paths["frame_00"])
    target_pts = read_kitti_bin(paths["frame_01"])  # 已含微小位姿差

    source = points_to_open3d(source_pts)
    target = points_to_open3d(target_pts)

    # 预处理：下采样加速 ICP
    voxel = 0.2
    source_ds = source.voxel_down_sample(voxel)
    target_ds = target.voxel_down_sample(voxel)

    # 估计法线（Point-to-Plane ICP 需要）
    source_ds.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30)
    )
    target_ds.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.5, max_nn=30)
    )

    threshold = 0.5  # 对应点最大距离
    init = np.eye(4)

    print("=== ICP 配准 ===")
    print(f"源点云: {len(source_ds.points)} 点 (下采样后)")
    print(f"目标点云: {len(target_ds.points)} 点 (下采样后)")

    # Point-to-Point ICP
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source_ds, target_ds, threshold, init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=50),
    )
    print(f"\nPoint-to-Point ICP:")
    print(f"  fitness={reg_p2p.fitness:.4f}  inlier_rmse={reg_p2p.inlier_rmse:.4f}")
    print(f"  变换矩阵:\n{np.array(reg_p2p.transformation)}")

    # Point-to-Plane ICP（通常更精确）
    reg_p2pl = o3d.pipelines.registration.registration_icp(
        source_ds, target_ds, threshold, init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=50),
    )
    print(f"\nPoint-to-Plane ICP:")
    print(f"  fitness={reg_p2pl.fitness:.4f}  inlier_rmse={reg_p2pl.inlier_rmse:.4f}")
    print(f"  变换矩阵:\n{np.array(reg_p2pl.transformation)}")

    # 应用配准结果
    source_aligned = source_ds.transform(reg_p2pl.transformation)
    source_aligned.paint_uniform_color([1, 0.3, 0.1])
    target_ds.paint_uniform_color([0.1, 0.6, 0.9])

    print("\n红色=配准后源点云, 蓝色=目标点云")
    o3d.visualization.draw_geometries(
        [source_aligned, target_ds],
        window_name="ICP 配准结果",
    )


if __name__ == "__main__":
    main()
