"""
07 点云拼接基础：变换矩阵（旋转 + 平移）
实践任务：对点云手动应用旋转矩阵和平移向量，观察坐标变化
预计时长：30 min
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import points_to_open3d, read_kitti_bin
from utils.sample_data import ensure_sample_data

# ---------------------------------------------------------------------------
# 刚体变换: P' = R @ P + t
#   R: 3×3 旋转矩阵
#   t: 3×1 平移向量
# 齐次坐标 4×4 变换矩阵:
#   T = [ R | t ]
#       [ 0 | 1 ]
# ---------------------------------------------------------------------------


def rotation_matrix_yaw(deg: float) -> np.ndarray:
    """绕 Z 轴旋转（车辆偏航角）。"""
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def make_transform(R: np.ndarray, t: np.ndarray) -> np.ndarray:
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t
    return T


def apply_transform(points: np.ndarray, T: np.ndarray) -> np.ndarray:
    """对 (N,3+) 点云应用 4×4 变换矩阵。"""
    xyz = points[:, :3]
    ones = np.ones((len(xyz), 1))
    homo = np.hstack([xyz, ones])          # (N, 4)
    transformed = (T @ homo.T).T[:, :3]    # (N, 3)
    result = points.copy()
    result[:, :3] = transformed
    return result


def main():
    import open3d as o3d

    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)
    points = read_kitti_bin(paths["frame_00"])

    # 定义变换：绕 Z 轴转 30°，平移 (2, 1, 0.5) 米
    R = rotation_matrix_yaw(30)
    t = np.array([2.0, 1.0, 0.5])
    T = make_transform(R, t)

    print("=== 变换矩阵 T (4×4) ===")
    np.set_printoptions(precision=3, suppress=True)
    print(T)

    # 取一个点观察坐标变化
    sample = points[0]
    print(f"\n原始点:  ({sample[0]:.3f}, {sample[1]:.3f}, {sample[2]:.3f})")
    transformed_pts = apply_transform(points, T)
    t_sample = transformed_pts[0]
    print(f"变换后:  ({t_sample[0]:.3f}, {t_sample[1]:.3f}, {t_sample[2]:.3f})")

    # 验证: R @ p + t
    manual = R @ sample[:3] + t
    print(f"手算验证: ({manual[0]:.3f}, {manual[1]:.3f}, {manual[2]:.3f})")

    # 可视化
    pcd_orig = points_to_open3d(points)
    pcd_trans = points_to_open3d(transformed_pts)
    pcd_orig.paint_uniform_color([0.3, 0.5, 0.9])
    pcd_trans.paint_uniform_color([0.9, 0.4, 0.1])

    coord_orig = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
    coord_trans = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
    coord_trans.transform(T)

    print("\n蓝色=原始, 橙色=变换后, 坐标轴显示各自位姿")
    o3d.visualization.draw_geometries(
        [pcd_orig, pcd_trans, coord_orig, coord_trans],
        window_name="刚体变换：旋转 + 平移",
    )


if __name__ == "__main__":
    main()
