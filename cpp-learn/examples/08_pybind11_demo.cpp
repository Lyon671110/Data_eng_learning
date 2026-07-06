/**
 * 实战项目 4：Python 与 C++ 联合编程 (Pybind11 示例)
 * 
 * 场景：写一个 C++ 高性能坐标系转换函数，打包给 Python 调用。
 * 注意：此文件需要 pybind11 依赖，通常用 CMake 编译。
 * 这里仅提供源码演示，展示 C++ 是如何暴露给 Python 的。
 */


// 取消注释后可用于实际编译
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // 让 C++ vector 自动转换成 Python list
#include <vector>

namespace py = pybind11;

// 一个简单的点云 3D 坐标
struct Point3D {
    double x, y, z;
};

// C++ 的高性能处理函数：假设把激光雷达的坐标转为相机坐标
std::vector<Point3D> transform_lidar_to_camera(const std::vector<Point3D>& points) {
    std::vector<Point3D> result;
    // 假设做了一个复杂的矩阵乘法
    for (const auto& p : points) {
        result.push_back({
            p.y * 1.5,
            -p.z * 1.2,
            p.x * 0.9
        });
    }
    return result;
}

// ==========================================
// 这段宏是 Pybind11 的核心：将 C++ 绑定到 Python
// ==========================================
PYBIND11_MODULE(my_cpp_module, m) {
    m.doc() = "自动驾驶数据闭环 C++ 加速算子"; // 模块的 docstring

    // 绑定结构体，让 Python 能认识 Point3D
    py::class_<Point3D>(m, "Point3D")
        .def(py::init<double, double, double>()) // 允许 Python 里 Point3D(x, y, z) 这样创建
        .def_readwrite("x", &Point3D::x)
        .def_readwrite("y", &Point3D::y)
        .def_readwrite("z", &Point3D::z);

    // 绑定函数
    m.def("transform_lidar_to_camera", &transform_lidar_to_camera, 
          "将激光雷达点云坐标转换到相机坐标系");
}


#include <iostream>

int main() {
    std::cout << "=== 项目4：Pybind11 联合编程源码示例 ===\n\n";
    std::cout << "   此项目主要展示 C++ 如何绑定到 Python。\n";
    std::cout << "   请查看 examples/08_pybind11_demo.cpp 的注释源码。\n";
    std::cout << "   实际开发中，会使用 CMake 将其编译为 .so 文件供 Python import。\n";
    return 0;
}
