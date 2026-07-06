"""生成合成点云数据，无需下载 KITTI 即可运行示例。"""

from pathlib import Path

import numpy as np

from utils.kitti_loader import save_kitti_bin


def _make_ground_plane(n: int = 8000, size: float = 30.0) -> np.ndarray:
    x = np.random.uniform(-size, size, n)
    y = np.random.uniform(-size, size, n)
    z = np.random.normal(0, 0.02, n)
    intensity = np.random.uniform(0.1, 0.4, n)
    return np.column_stack([x, y, z, intensity])


def _make_objects() -> np.ndarray:
    """几个简单几何体：柱子 + 墙面。"""
    parts = []
    # 圆柱（树干/柱子）
    for cx, cy in [(5, 3), (-4, 6), (8, -5)]:
        theta = np.random.uniform(0, 2 * np.pi, 400)
        r = np.random.uniform(0, 0.4, 400)
        x = cx + r * np.cos(theta)
        y = cy + r * np.sin(theta)
        z = np.random.uniform(0, 3, 400)
        intensity = np.full(400, 0.8)
        parts.append(np.column_stack([x, y, z, intensity]))
    # 墙面
    wall_y = np.full(600, 10.0)
    wall_x = np.random.uniform(-10, 10, 600)
    wall_z = np.random.uniform(0, 2.5, 600)
    wall_i = np.full(600, 0.6)
    parts.append(np.column_stack([wall_x, wall_y, wall_z, wall_i]))
    return np.vstack(parts)


def _add_noise(points: np.ndarray, ratio: float = 0.03) -> np.ndarray:
    n_noise = int(len(points) * ratio)
    noise = np.random.uniform(-25, 25, (n_noise, 3))
    noise_i = np.random.uniform(0, 1, n_noise)
    noise_pts = np.column_stack([noise, noise_i])
    return np.vstack([points, noise_pts])


def generate_sample_frame(seed: int = 0) -> np.ndarray:
    np.random.seed(seed)
    pts = np.vstack([_make_ground_plane(), _make_objects()])
    return pts.astype(np.float32)


def generate_noisy_frame(seed: int = 1) -> np.ndarray:
    pts = generate_sample_frame(seed)
    return _add_noise(pts).astype(np.float32)


def generate_second_frame(seed: int = 0, yaw_deg: float = 2.0, tx: float = 0.3) -> np.ndarray:
    """生成与第一帧略有位姿差异的第二帧（用于 ICP 练习）。"""
    pts = generate_sample_frame(seed)
    yaw = np.radians(yaw_deg)
    c, s = np.cos(yaw), np.sin(yaw)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    xyz = pts[:, :3] @ R.T + np.array([tx, 0.05, 0.0])
    result = pts.copy()
    result[:, :3] = xyz
    return result.astype(np.float32)


def ensure_sample_data(data_dir: str | Path) -> dict[str, Path]:
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "frame_00": data_dir / "000000.bin",
        "frame_01": data_dir / "000001.bin",
        "noisy": data_dir / "noisy.bin",
    }
    if not paths["frame_00"].exists():
        save_kitti_bin(paths["frame_00"], generate_sample_frame(0))
    if not paths["frame_01"].exists():
        save_kitti_bin(paths["frame_01"], generate_second_frame(0))
    if not paths["noisy"].exists():
        save_kitti_bin(paths["noisy"], generate_noisy_frame(1))
    return paths
