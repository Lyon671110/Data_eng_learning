# C++ 学习项目 Makefile
# 用法: make <目标名>  或  make run-<目标名>

CXX      := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -g -O0 -pthread
BUILD    := build

EXAMPLES := 01_pointers 02_references 03_stl 04_raii 05_mock_bag_parser 06_trajectory_filter 07_sensor_sync 08_pybind11_demo 09_multithreading_basic 10_mutex_and_locks

.PHONY: all clean help $(EXAMPLES) $(addprefix run-,$(EXAMPLES))

all: $(EXAMPLES)

help:
	@echo "C++ 学习项目 - 可用命令:"
	@echo "  make all              编译所有示例"
	@echo "  make 01_pointers      编译指针示例"
	@echo "  make 02_references    编译引用示例"
	@echo "  make 03_stl           编译 STL 示例"
	@echo "  make 04_raii          编译 RAII 示例"
	@echo "  make 05_mock_bag_parser 编译数据解析实战"
	@echo "  make 06_trajectory_filter 编译轨迹清洗实战"
	@echo "  make 07_sensor_sync   编译传感器同步实战"
	@echo "  make 08_pybind11_demo 编译 Pybind11 演示"
	@echo "  make 09_multithreading_basic 编译多线程基础"
	@echo "  make 10_mutex_and_locks      编译互斥锁实战"
	@echo "  make run-01_pointers  编译并运行指针示例"
	@echo "  make run-02_references 编译并运行引用示例"
	@echo "  make run-03_stl       编译并运行 STL 示例"
	@echo "  make run-04_raii      编译并运行 RAII 示例"
	@echo "  make run-05_mock_bag_parser 编译并运行数据解析实战"
	@echo "  make run-06_trajectory_filter 编译并运行轨迹清洗实战"
	@echo "  make run-07_sensor_sync   编译并运行传感器同步实战"
	@echo "  make run-08_pybind11_demo 编译并运行 Pybind 演示"
	@echo "  make run-09_multithreading_basic 编译并运行多线程基础"
	@echo "  make run-10_mutex_and_locks      编译并运行互斥锁实战"
	@echo "  make clean            清理编译产物"

$(EXAMPLES): %: examples/%.cpp
	@mkdir -p $(BUILD)
	$(CXX) $(CXXFLAGS) $< -o $(BUILD)/$@
	@echo "✓ 编译成功: $(BUILD)/$@"

$(addprefix run-,$(EXAMPLES)): run-%: %
	@echo "---------- 运行 $* ----------"
	./$(BUILD)/$*

clean:
	rm -rf $(BUILD)
