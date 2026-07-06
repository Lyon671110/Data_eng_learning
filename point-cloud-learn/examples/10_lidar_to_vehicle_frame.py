"""
10 点云投影到车辆坐标系
实践任务：利用已知外参将 LiDAR 点云变换到车辆坐标系下
预计时长：30 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin
from utils.sample_data import ensure_sample_data

# ---------------------------------------------------------------------------
# 外参 (Extrinsic): 描述传感器坐标系 → 车辆坐标系的刚体变换
#   P_vehicle = R @ P_lidar + t
#   或齐次形式: P_v = T_lidar_to_vehicle @ P_l
#
# KITTI 数据集提供 calib_velo_to_cam 等标定文件
# 本示例使用模拟外参：LiDAR 安装在车顶 (1.2, 0, 1.8)m，无旋转
# ---------------------------------------------------------------------------


def make_extrinsic(translation: np.ndarray, rotation: np.ndarray | None = None) -> np.ndarray:
    T = np.eye(4)
    T[:3, :3] = rotation if rotation is not None else np.eye(3)
    T[:3, 3] = translation
    return T


def transform_points(points: np.ndarray, T: np.ndarray) -> np.ndarray:
    xyz = points[:, :3]
    ones = np.ones((len(xyz), 1))
    homo = np.hstack([xyz, ones])
    new_xyz = (T @ homo.T).T[:, :3]
    result = points.copy()
    result[:, :3] = new_xyz
    return result


def main():
    import open3d as o3d

    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)
    points_lidar = read_kitti_bin(paths["frame_00"])

    # 模拟外参: LiDAR → base_link
    # 实际项目中从标定文件读取
    t_lidar_to_vehicle = np.array([1.2, 0.0, 1.8])
    R_lidar_to_vehicle = np.eye(3)
    T_lidar_to_vehicle = make_extrinsic(t_lidar_to_vehicle, R_lidar_to_vehicle)

    print("=== LiDAR → 车辆坐标系 外参 ===")
    np.set_printoptions(precision=3, suppress=True)
    print(T_lidar_to_vehicle)
    print(f"含义: LiDAR 原点在车辆坐标系下位置 = {t_lidar_to_vehicle}")

    points_vehicle = transform_points(points_lidar, T_lidar_to_vehicle)

    # 对比 Z 坐标变化（LiDAR 在车顶，变换后地面点 Z 应更低）
    print(f"\nLiDAR 坐标系 Z 范围: [{points_lidar[:, 2].min():.2f}, {points_lidar[:, 2].max():.2f}]")
    print(f"车辆坐标系 Z 范围:   [{points_vehicle[:, 2].min():.2f}, {points_vehicle[:, 2].max():.2f}]")

    pcd_lidar = points_to_open3d(points_lidar)
    pcd_vehicle = points_to_open3d(points_vehicle)
    pcd_lidar.paint_uniform_color([0.2, 0.6, 1.0])
    pcd_vehicle.paint_uniform_color([1.0, 0.5, 0.1])

    # 车辆坐标系原点
    coord_vehicle = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
    coord_lidar = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.8)
    coord_lidar.transform(T_lidar_to_vehicle)

    print("\n蓝色=LiDAR 坐标系点云, 橙色=车辆坐标系点云")
    print("坐标轴: 大=base_link, 小=lidar_link")
    o3d.visualization.draw_geometries(
        [pcd_lidar, pcd_vehicle, coord_vehicle, coord_lidar],
        window_name="LiDAR → 车辆坐标系变换",
    )


if __name__ == "__main__":
    main()
