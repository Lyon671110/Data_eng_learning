# C++ 学习环境

用于学习 **指针**、**引用**、**STL** 和 **RAII** 的动手练习项目。

## 环境要求

- g++ 11+ (已安装: `g++ --version`)
- make

## 快速开始

```bash
cd ~/cpp-learn

# 编译并运行所有示例
make all
make run-01_pointers
make run-02_references
make run-03_stl
make run-04_raii

# 或单独编译
make 01_pointers
./build/01_pointers
```

## 学习路线

| 文件 | 主题 | 核心概念 |
|------|------|----------|
| `examples/01_pointers.cpp` | 指针 | `&` 取地址, `*` 解引用, `new/delete`, 指针传参 |
| `examples/02_references.cpp` | 引用 | `类型&`, const 引用, 引用传参, 右值引用 |
| `examples/03_stl.cpp` | STL | vector, string, map, set, 迭代器, algorithm |
| `examples/04_raii.cpp` | RAII | 析构自动释放, FileGuard, unique_ptr, lock_guard |
| `examples/05_mock_bag_parser.cpp` | 实战项目1 | 二进制文件I/O, struct, vector存取, Lambda自定义排序 |
| `examples/06_trajectory_filter.cpp` | 实战项目2 | 引用传递, RAII 封装日志, 数据过滤 |
| `examples/07_sensor_sync.cpp` | 实战项目3 | std::map 底层特性, lower_bound 二分查找寻优 |
| `examples/08_pybind11_demo.cpp` | 实战项目4 | Python/C++ 联合编程展示 (Pybind11 语法) |
| `examples/09_multithreading_basic.cpp` | 多线程 | `std::thread`, 并发执行, `join()`, `chrono` 时间控制 |
| `examples/10_mutex_and_locks.cpp` | 互斥锁 | 资源竞争, `std::mutex`, `std::lock_guard` RAII加锁 |

## 使用 CMake 构建 (工业界标准)

除了 `make`，本项目现已支持更标准的 **CMake** 构建方式。强烈建议使用这种方式：

```bash
# 1. 生成构建配置 (会在 build 目录下生成 Makefile)
cmake -B build

# 2. 开始编译
cmake --build build

# 3. 运行编译好的程序 (例如多线程示例)
./build/09_multithreading_basic
```

## 常用命令

```bash
# 直接编译单个文件
g++ -std=c++17 -Wall -g examples/01_pointers.cpp -o build/01_pointers

# 调试 (需要 gdb)
gdb ./build/01_pointers

# 清理
make clean
```

## 练习建议

1. 先运行示例, 阅读输出
2. 修改代码中的数值, 观察变化
3. 故意写错 (如解引用空指针), 看编译器/运行时报什么错
4. 自己写一个小程序: 用 vector 存学生成绩, 用 map 按姓名查找

## 推荐下一步

- 智能指针: `examples/04_raii.cpp` 中的 `unique_ptr`, `shared_ptr` 对比见文档
- 现代 C++: 范围 for、auto、结构化绑定
- LeetCode 用 C++ 刷题巩固
