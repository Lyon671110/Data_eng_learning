"""
02 日志 ETL 完整流水线
实践任务：读取 access.log → 解析 → 过滤 GET/200 → 按 IP 统计 → 写 Parquet → 读回验证
预计时长：45 min

数据流:
  access.log (text)
    → read.text
    → select/split 解析字段
    → filter (method=GET, status=200)
    → groupBy(ip).count()
    → orderBy(request_count DESC)
    → write.parquet
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pyspark.sql.functions import col, count, split

from utils.sample_data import ensure_sample_data
from utils.spark_session import create_local_session

# ---------------------------------------------------------------------------
# 日志格式（每行空格分隔）:
#   IP  METHOD  PATH  STATUS  RESPONSE_MS
# 示例:
#   192.168.1.1 GET /api/users 200 1250
# ---------------------------------------------------------------------------


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)


def build_pipeline(spark, log_path: Path):
    """构建 ETL 逻辑计划（懒执行，此时不会真正计算）。"""
    logs = spark.read.text(str(log_path))

    parsed = logs.select(
        split(col("value"), " ").getItem(0).alias("ip"),
        split(col("value"), " ").getItem(1).alias("method"),
        split(col("value"), " ").getItem(2).alias("path"),
        split(col("value"), " ").getItem(3).cast("int").alias("status"),
        split(col("value"), " ").getItem(4).cast("int").alias("response_ms"),
    )

    filtered = parsed.filter((col("method") == "GET") & (col("status") == 200))

    ip_counts = (
        filtered
        .groupBy("ip")
        .agg(count("*").alias("request_count"))
        .orderBy(col("request_count").desc())
    )

    return logs, parsed, filtered, ip_counts


def main():
    parser = argparse.ArgumentParser(description="日志 ETL：text → Parquet")
    parser.add_argument(
        "--lines",
        type=int,
        default=10_000,
        help="若自动生成日志，写入的行数（默认 10000）",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    output_dir = root / "output" / "ip_counts"

    log_path = ensure_sample_data(data_dir, num_lines=args.lines)
    file_size_kb = log_path.stat().st_size / 1024

    print_section("阶段 0：准备数据")
    print(f"日志路径: {log_path}")
    print(f"文件大小: {file_size_kb:.1f} KB")
    print("字段格式: ip method path status response_ms")

    spark = create_local_session("log-etl-pipeline")
    logs, parsed, filtered, ip_counts = build_pipeline(spark, log_path)

    print_section("阶段 1：Extract — read.text")
    print("Spark 按块并行读取文本，每行放入 value 列")
    print("schema:", logs.schema.simpleString())
    raw_count = logs.count()
    print(f"原始行数: {raw_count:,}")
    print("样例（前 3 行）:")
    logs.show(3, truncate=60)

    print_section("阶段 2：Transform ① — select + split 解析")
    print("将 value 拆成 ip / method / path / status / response_ms")
    print("schema:", parsed.schema.simpleString())
    parsed.show(5, truncate=False)

    print_section("阶段 3：Transform ② — filter")
    print("保留 method=GET 且 status=200 的记录")
    filtered_count = filtered.count()
    print(f"过滤后行数: {filtered_count:,}（保留率 {filtered_count / raw_count:.1%}）")
    filtered.show(5, truncate=False)

    print_section("阶段 4：Transform ③ — groupBy + count（Shuffle）")
    print("按 ip 分组计数；相同 ip 的记录会 shuffle 到同一分区")
    ip_counts.show(10, truncate=False)

    print_section("阶段 5：Load — write.parquet")
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)

    ip_counts.write.mode("overwrite").parquet(str(output_dir))

    parquet_files = sorted(output_dir.glob("*.parquet"))
    parquet_size_kb = sum(f.stat().st_size for f in parquet_files) / 1024
    print(f"输出目录: {output_dir}")
    print(f"Parquet 文件数: {len(parquet_files)}")
    print(f"Parquet 总大小: {parquet_size_kb:.1f} KB")
    print(f"压缩比（相对原始日志）: {file_size_kb / max(parquet_size_kb, 0.1):.1f}x")

    print_section("阶段 6：验证 — 读回 Parquet")
    result = spark.read.parquet(str(output_dir))
    result_count = result.count()
    print(f"读回行数: {result_count:,}")
    print("Top 10 IP:")
    result.show(10, truncate=False)

    print_section("数据量变化总结")
    print(f"  access.log     → {raw_count:>8,} 行  (~{file_size_kb:.0f} KB 文本)")
    print(f"  过滤后          → {filtered_count:>8,} 行")
    print(f"  ip_counts      → {result_count:>8,} 行  (~{parquet_size_kb:.0f} KB Parquet)")

    spark.stop()
    print("\n完成。可用以下命令查看 Parquet 目录:")
    print(f"  ls -lh {output_dir}")


if __name__ == "__main__":
    main()
