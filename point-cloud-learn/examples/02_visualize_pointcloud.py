"""
02 3D 可视化基础
实践任务：用 matplotlib 或 Open3D 绘制点云散点图
预计时长：30 min
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.kitti_loader import read_kitti_bin, points_to_open3d
from utils.sample_data import ensure_sample_data
from utils.visualize import should_show_interactive, show_geometries


def visualize_matplotlib(points: np.ndarray, max_points: int = 5000):
    """Matplotlib 3D 散点图（适合快速预览，大点云需下采样）。"""
    xyz = points[:, :3]
    intensity = points[:, 3] if points.shape[1] >= 4 else None

    if len(xyz) > max_points:
        idx = np.random.choice(len(xyz), max_points, replace=False)
        xyz = xyz[idx]
        intensity = intensity[idx] if intensity is not None else None

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    colors = intensity if intensity is not None else xyz[:, 2]
    sc = ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c=colors, s=0.3, cmap="viridis")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("Matplotlib 点云散点图")
    plt.colorbar(sc, ax=ax, shrink=0.6, label="intensity / height")
    plt.tight_layout()
    out = Path(__file__).parent.parent / "output" / "02_matplotlib.png"
    out.parent.mkdir(exist_ok=True)
    plt.savefig(out, dpi=120)
    print(f"Matplotlib 图已保存: {out}")
    if should_show_interactive():
        plt.show()
    else:
        plt.close(fig)


def visualize_open3d(points: np.ndarray):
    """Open3D 交互式可视化（可旋转/缩放）。"""
    import open3d as o3d

    pcd = points_to_open3d(points)
    print(f"Open3D 点数: {len(pcd.points)}")
    out = Path(__file__).parent.parent / "output" / "02_open3d.png"
    show_geometries([pcd], window_name="Open3D 点云可视化", output_path=out)


def main():
    data_dir = Path(__file__).parent.parent / "data"
    paths = ensure_sample_data(data_dir)
    points = read_kitti_bin(paths["frame_00"])

    print("=== 方式 1: Matplotlib ===")
    visualize_matplotlib(points)

    print("\n=== 方式 2: Open3D（交互式）===")
    visualize_open3d(points)


if __name__ == "__main__":
    main()
