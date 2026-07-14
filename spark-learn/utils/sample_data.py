"""生成合成 Web 访问日志，无需下载真实数据即可运行示例。"""

import random
from pathlib import Path

IPS = [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3",
    "10.0.0.5",
    "10.0.0.8",
    "172.16.0.10",
]

METHODS = ["GET", "POST", "PUT", "DELETE"]
PATHS = [
    "/api/users",
    "/api/orders",
    "/api/login",
    "/api/products",
    "/api/cart",
    "/home",
    "/static/css/main.css",
]
STATUSES = [200, 200, 200, 200, 404, 500]


def _make_log_line(rng: random.Random) -> str:
    ip = rng.choice(IPS)
    method = rng.choices(METHODS, weights=[70, 20, 5, 5], k=1)[0]
    path = rng.choice(PATHS)
    status = rng.choice(STATUSES)
    response_ms = rng.randint(50, 3000)
    return f"{ip} {method} {path} {status} {response_ms}"


def generate_access_log(num_lines: int = 10_000, seed: int = 42) -> list[str]:
    rng = random.Random(seed)
    return [_make_log_line(rng) for _ in range(num_lines)]


def ensure_sample_data(data_dir: str | Path, *, num_lines: int = 10_000) -> Path:
    """确保 data/access.log 存在；不存在则自动生成。"""
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    log_path = data_dir / "access.log"

    if not log_path.exists():
        lines = generate_access_log(num_lines=num_lines)
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return log_path
