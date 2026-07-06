"""KITTI 点云读取与格式说明工具。"""

from pathlib import Path

import numpy as np


def read_kitti_bin(path: str | Path) -> np.ndarray:
    """
    读取 KITTI Velodyne .bin 文件。

  KITTI 格式：每个点 4 个 float32 → [x, y, z, intensity]
  返回 shape (N, 4) 的 numpy 数组。
    """
    points = np.fromfile(path, dtype=np.float32)
    return points.reshape(-1, 4)


def points_to_open3d(points: np.ndarray):
    """将 (N, 3) 或 (N, 4) 数组转为 Open3D PointCloud。"""
    import open3d as o3d

    xyz = points[:, :3]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    if points.shape[1] >= 4:
        intensity = points[:, 3]
        # 将 intensity 归一化后映射为灰度颜色
        i_min, i_max = intensity.min(), intensity.max()
        if i_max > i_min:
            norm = (intensity - i_min) / (i_max - i_min)
        else:
            norm = np.zeros_like(intensity)
        colors = np.stack([norm, norm, norm], axis=1)
        pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd


def save_kitti_bin(path: str | Path, points: np.ndarray) -> None:
    """保存为 KITTI .bin 格式。"""
    points.astype(np.float32).tofile(path)
