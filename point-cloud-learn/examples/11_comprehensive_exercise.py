"""
11 综合练习
实践任务：加载连续两帧 KITTI 点云，去噪、下采样、ICP 配准，
         输出变换矩阵和配准后点云
预计时长：90 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin, save_kitti_bin
from utils.sample_data import ensure_sample_data


def preprocess(pcd, voxel_size=0.2, sor_neighbors=20, sor_std=2.0):
    """去噪 + 下采样预处理流水线。"""
    print(f"  原始点数: {len(pcd.points)}")
    pcd, _ = pcd.remove_statistical_outlier(
        nb_neighbors=sor_neighbors, std_ratio=sor_std
    )
    print(f"  SOR 后:   {len(pcd.points)}")
    pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    print(f"  下采样后: {len(pcd.points)}")
    pcd.estimate_normals(
        search_param=__import__("open3d").geometry.KDTreeSearchParamHybrid(
            radius=0.5, max_nn=30
        )
    )
    return pcd


def run_icp(source, target, threshold=0.5, max_iter=50):
    import open3d as o3d

    init = np.eye(4)
    result = o3d.pipelines.registration.registration_icp(
        source, target, threshold, init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=max_iter),
    )
    return result


def main():
    import open3d as o3d

    data_dir = Path(__file__).parent.parent / "data"
    out_dir = Path(__file__).parent.parent / "output"
    out_dir.mkdir(exist_ok=True)
    paths = ensure_sample_data(data_dir)

    print("=" * 60)
    print("综合练习：两帧点云配准流水线")
    print("=" * 60)

    # --- Step 1: 加载连续两帧 ---
    print("\n[Step 1] 加载点云")
    frame0 = read_kitti_bin(paths["frame_00"])
    frame1 = read_kitti_bin(paths["frame_01"])
    pcd0 = points_to_open3d(frame0)
    pcd1 = points_to_open3d(frame1)
    print(f"  帧 0: {len(pcd0.points)} 点")
    print(f"  帧 1: {len(pcd1.points)} 点")

    # --- Step 2: 预处理 ---
    print("\n[Step 2] 帧 0 预处理 (SOR + 体素下采样)")
    src = preprocess(pcd0)
    print("\n[Step 2] 帧 1 预处理 (SOR + 体素下采样)")
    tgt = preprocess(pcd1)

    # --- Step 3: ICP 配准 ---
    print("\n[Step 3] ICP 配准 (帧 0 → 帧 1)")
    reg = run_icp(src, tgt)
    T = np.array(reg.transformation)

    print(f"  fitness:     {reg.fitness:.4f}")
    print(f"  inlier_rmse: {reg.inlier_rmse:.4f}")
    print(f"  变换矩阵 T:\n{T}")

    # --- Step 4: 应用变换，保存结果 ---
    print("\n[Step 4] 保存配准结果")
    src_aligned = src.transform(T)
    src_aligned.paint_uniform_color([1.0, 0.3, 0.1])
    tgt.paint_uniform_color([0.1, 0.5, 0.9])

    # 合并配准后点云
    merged = src_aligned + tgt
    merged_path = out_dir / "aligned_merged.pcd"
    o3d.io.write_point_cloud(str(merged_path), merged)
    print(f"  合并点云: {merged_path}  ({len(merged.points)} 点)")

    T_path = out_dir / "icp_transform.txt"
    np.savetxt(T_path, T, fmt="%.6f")
    print(f"  变换矩阵: {T_path}")

    # 保存配准后的完整帧 0（未下采样版）
    pcd0_full_aligned = points_to_open3d(frame0).transform(T)
    aligned_bin = out_dir / "frame_00_aligned.bin"
    aligned_pts = np.asarray(pcd0_full_aligned.points)
    intensity = frame0[:, 3:4]
    save_kitti_bin(aligned_bin, np.hstack([aligned_pts, intensity]))
    print(f"  配准后帧 0: {aligned_bin}")

    # --- Step 5: 可视化 ---
    print("\n[Step 5] 可视化 (红色=配准后帧0, 蓝色=帧1)")
    o3d.visualization.draw_geometries(
        [src_aligned, tgt],
        window_name="综合练习 - ICP 配准结果",
    )

    print("\n" + "=" * 60)
    print("完成！输出文件在 point-cloud-learn/output/ 目录")
    print("=" * 60)


if __name__ == "__main__":
    main()
