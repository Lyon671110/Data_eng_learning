"""
09 坐标系与 TF 树：传感器坐标系、车辆坐标系
实践任务：画出简化的传感器安装位置示意图，标注坐标系
预计时长：20 min
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle
from mpl_toolkits.mplot3d import proj3d

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.visualize import should_show_interactive

# ---------------------------------------------------------------------------
# 自动驾驶常见坐标系:
#   - 车辆坐标系 (base_link): 原点通常在车辆后轴中心, X前 Y左 Z上 (ROS 惯例)
#   - LiDAR 坐标系: 原点在雷达光心, 轴向因安装而异
#   - 相机坐标系: 原点在光心, Z 轴沿光轴向前
# TF 树: 描述各坐标系之间的父子关系与变换
#   base_link → lidar_link → (点云数据在此坐标系)
#   base_link → camera_link
# ---------------------------------------------------------------------------


class Arrow3D(FancyArrowPatch):
    """3D 箭头辅助类。"""

    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = [xs, ys, zs]

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def draw_frame(ax, origin, R, label, scale=0.8):
    """在 3D 图中绘制坐标系（R 的列向量即各轴方向）。"""
    colors = ["r", "g", "b"]
    axis_names = ["X", "Y", "Z"]
    for i in range(3):
        direction = R[:, i] * scale
        end = origin + direction
        arrow = Arrow3D(
            [origin[0], end[0]], [origin[1], end[1]], [origin[2], end[2]],
            mutation_scale=12, lw=2, arrowstyle="-|>", color=colors[i],
        )
        ax.add_artist(arrow)
        ax.text(end[0], end[1], end[2], axis_names[i], color=colors[i], fontsize=9)
    ax.text(origin[0], origin[1], origin[2] - 0.3, label, fontsize=10, ha="center")


def draw_vehicle_topdown(ax):
    """俯视图：车辆与传感器安装位置。"""
    # 车辆轮廓
    car = Rectangle((-2.0, -0.9), 4.5, 1.8, linewidth=2, edgecolor="black", facecolor="lightgray", alpha=0.5)
    ax.add_patch(car)
    ax.annotate("base_link\n(后轴中心)", (-0.5, 0), fontsize=9, ha="center")

    sensors = {
        "LiDAR\n(车顶)": (1.2, 0, "^", "red"),
        "前相机": (2.0, 0, "s", "blue"),
        "左相机": (0.5, 0.8, "s", "green"),
        "右相机": (0.5, -0.8, "s", "green"),
        "后雷达": (-1.8, 0, "o", "orange"),
    }
    for name, (x, y, marker, color) in sensors.items():
        ax.plot(x, y, marker=marker, color=color, markersize=10)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(0, 12), ha="center", fontsize=8)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.set_xlabel("X 前方 (m)")
    ax.set_ylabel("Y 左侧 (m)")
    ax.set_title("俯视图：传感器安装位置")
    ax.grid(True, alpha=0.3)


def main():
    fig = plt.figure(figsize=(14, 6))

    # --- 左图：俯视图 ---
    ax1 = fig.add_subplot(121)
    draw_vehicle_topdown(ax1)

    # --- 右图：3D 坐标系关系 ---
    ax2 = fig.add_subplot(122, projection="3d")

    # base_link 坐标系（车辆）
    R_base = np.eye(3)
    draw_frame(ax2, np.array([0, 0, 0]), R_base, "base_link", scale=1.0)

    # LiDAR 外参：车顶前方，高度 1.8m，无旋转
    T_lidar = np.array([1.2, 0.0, 1.8])
    R_lidar = np.eye(3)
    draw_frame(ax2, T_lidar, R_lidar, "lidar", scale=0.6)

    # 前相机外参：前保险杠，略向下俯仰 15°
    pitch = np.radians(-15)
    R_cam = np.array([
        [1, 0, 0],
        [0, np.cos(pitch), -np.sin(pitch)],
        [0, np.sin(pitch), np.cos(pitch)],
    ])
    T_cam = np.array([2.0, 0.0, 0.5])
    draw_frame(ax2, T_cam, R_cam, "camera", scale=0.5)

    # 连线表示 TF 关系
    ax2.plot([0, T_lidar[0]], [0, T_lidar[1]], [0, T_lidar[2]], "k--", alpha=0.4)
    ax2.plot([0, T_cam[0]], [0, T_cam[1]], [0, T_cam[2]], "k--", alpha=0.4)

    ax2.set_xlabel("X (m)")
    ax2.set_ylabel("Y (m)")
    ax2.set_zlabel("Z (m)")
    ax2.set_title("3D 坐标系与 TF 关系")

    out = Path(__file__).parent.parent / "output" / "09_coordinate_frames.png"
    out.parent.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"示意图已保存: {out}")

    print("\n=== TF 树结构 ===")
    print("  map")
    print("   └── odom")
    print("        └── base_link  (车辆坐标系)")
    print("             ├── lidar_link  → 点云数据")
    print("             ├── camera_front_link")
    print("             ├── camera_left_link")
    print("             └── camera_right_link")

    if should_show_interactive():
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
