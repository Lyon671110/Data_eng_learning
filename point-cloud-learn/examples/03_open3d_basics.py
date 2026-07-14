"""
03 Open3D 入门：点云读写、显示、基本操作
实践任务：加载官方示例点云，尝试旋转/缩放视图
预计时长：20 min
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.visualize import show_geometries


def main():
    import open3d as o3d
    import numpy as np

    # --- 1. 加载 Open3D 内置示例点云 ---
    print("加载 Open3D 内置 DemoICPPointClouds ...")
    demo = o3d.data.DemoICPPointClouds()
    source = o3d.io.read_point_cloud(str(demo.paths[0]))
    print(f"  点数: {len(source.points)}")
    print(f"  是否有颜色: {source.has_colors()}")
    print(f"  是否有法线: {source.has_normals()}")

    # --- 2. 基本属性访问 ---
    pts = np.asarray(source.points)
    print(f"  坐标范围 X: [{pts[:, 0].min():.2f}, {pts[:, 0].max():.2f}]")
    print(f"  坐标范围 Y: [{pts[:, 1].min():.2f}, {pts[:, 1].max():.2f}]")
    print(f"  坐标范围 Z: [{pts[:, 2].min():.2f}, {pts[:, 2].max():.2f}]")

    # --- 3. 读写本地文件 ---
    out_dir = Path(__file__).parent.parent / "output"
    out_dir.mkdir(exist_ok=True)
    pcd_path = out_dir / "demo_cloud.pcd"
    o3d.io.write_point_cloud(str(pcd_path), source)
    loaded = o3d.io.read_point_cloud(str(pcd_path))
    print(f"\n已保存并重新加载: {pcd_path}  点数={len(loaded.points)}")

    # --- 4. 交互式可视化（旋转/缩放/平移）---
    print("\n=== 交互操作指南 ===")
    print("  鼠标左键拖动  → 旋转视角")
    print("  鼠标滚轮      → 缩放")
    print("  鼠标右键拖动  → 平移")
    print("  +/- 键        → 调整点大小")
    print("  Q / Esc       → 退出")

    # 给点云上色便于观察旋转效果
    source.paint_uniform_color([0.2, 0.6, 0.9])

    # 添加坐标系辅助（红=X, 绿=Y, 蓝=Z）
    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5)

    show_geometries(
        [source, coord],
        window_name="Open3D 入门 - 旋转/缩放练习",
        output_path=Path(__file__).parent.parent / "output" / "03_open3d_basics.png",
    )


if __name__ == "__main__":
    main()
