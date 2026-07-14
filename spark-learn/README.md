# Spark Learning

Spark 学习模块，从日志 ETL 入手理解 DataFrame 转换、Shuffle 聚合与 Parquet 输出。

## 环境准备

需要：

- [Poetry](https://python-poetry.org/) 2.x
- **Java 8+**（PySpark 依赖 JVM，推荐 Java 11）

```bash
java -version   # 确认已安装
cd spark-learn
poetry install
```

## 学习路线

| 编号 | 文件 | 主题 | 时长 | 实践任务 |
|------|------|------|------|----------|
| 02 | `examples/02_log_etl.py` | 日志 ETL 完整流水线 | 45 min | 读 access.log → 解析/过滤/聚合 → 写 Parquet → 读回验证 |

## 快速运行

```bash
cd spark-learn

# 默认生成 10000 行合成日志并跑完整 ETL
poetry run python examples/02_log_etl.py

# 指定日志行数（更大数据可感受 Spark 并行优势）
poetry run python examples/02_log_etl.py --lines 100000
```

首次运行会自动在 `data/` 生成 `access.log`（无需下载真实数据）。

## 流水线概览

```
access.log (text)
    ↓ read.text              Extract：按块并行读取
    ↓ select + split         Transform：解析 ip/method/path/status
    ↓ filter                 Transform：GET + status=200
    ↓ groupBy + count        Transform：按 IP 统计（Shuffle）
    ↓ orderBy                Transform：按访问量降序
    ↓ write.parquet          Load：列式存储输出
output/ip_counts/
```

## 目录结构

```
spark-learn/
├── README.md
├── pyproject.toml
├── data/                # 自动生成的 access.log
├── output/              # ETL 输出（ip_counts Parquet）
├── utils/
│   ├── sample_data.py   # 合成日志生成
│   └── spark_session.py # 本地 SparkSession 配置
└── examples/
    └── 02_log_etl.py
```

## 核心概念速查

### 懒执行（Lazy Evaluation）

`select`、`filter`、`groupBy` 只构建逻辑计划；遇到 `count`、`show`、`write` 才真正执行。

### Shuffle

`groupBy`、`orderBy`、`join` 会按 key 重新分区，是大数据作业的主要性能瓶颈。

### Parquet

列式存储格式，只读需要的列，压缩率高，Spark / Hive / Presto 均可直接查询。

### 本地模式 vs 集群

本模块使用 `local[*]` 在单机多核运行，代码与集群部署一致，便于学习；生产环境将 `master` 改为 `yarn` 或 `k8s://...` 即可。
