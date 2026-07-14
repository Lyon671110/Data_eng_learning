"""本地 SparkSession 工厂，统一示例脚本的 Spark 配置。"""

import os

from pyspark.sql import SparkSession


def create_local_session(app_name: str, *, quiet: bool = True) -> SparkSession:
    """创建本地模式 SparkSession（无需集群）。"""
    if quiet:
        os.environ.setdefault("PYSPARK_SUBMIT_ARGS", "--conf spark.ui.showConsoleProgress=false pyspark-shell")

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.driver.memory", "1g")
    )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
