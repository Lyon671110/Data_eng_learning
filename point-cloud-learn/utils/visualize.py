"""Open3D 可视化工具：支持交互窗口 / 离屏渲染 / 跳过显示。"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def should_show_interactive() -> bool:
    """是否弹出交互窗口。可通过环境变量或 --no-viz 关闭。"""
    if "--no-viz" in sys.argv:
        return False
    return os.environ.get("OPEN3D_HEADLESS", "").lower() not in ("1", "true", "yes")


def render_offscreen(geometries, output_path: str | Path) -> None:
    """离屏渲染并保存 PNG，不弹窗、不阻塞。"""
    import open3d as o3d

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False, width=1280, height=720)
    for geom in geometries:
        vis.add_geometry(geom)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(str(output_path))
    vis.destroy_window()
    print(f"已保存渲染图: {output_path}")


def show_geometries(
    geometries,
    window_name: str = "Open3D",
    output_path: str | Path | None = None,
) -> None:
    """
    显示点云。默认交互窗口；加 --no-viz 或 OPEN3D_HEADLESS=1 时改为离屏保存 PNG。

    交互操作: 左键旋转 | 滚轮缩放 | 右键平移 | Q 或 Esc 关闭
    """
    import open3d as o3d

    if output_path is None:
        output_path = Path("output") / "open3d_render.png"

    if not should_show_interactive():
        render_offscreen(geometries, output_path)
        return

    print("操作提示: 左键旋转 | 滚轮缩放 | 右键平移 | Q/Esc 关闭窗口")
    print("若窗口无法关闭: 终端 Ctrl+C，或重新运行时加 --no-viz")
    o3d.visualization.draw_geometries(geometries, window_name=window_name)
