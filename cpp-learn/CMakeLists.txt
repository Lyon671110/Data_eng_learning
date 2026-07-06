# 这是 CMake 的配置文件：CMakeLists.txt
# 它是目前 C++ 工业界最主流的构建系统。它会自动帮你生成复杂的 Makefile。

# 1. 指定需要的 CMake 最低版本
cmake_minimum_required(VERSION 3.10)

# 2. 定义项目名称
project(AutoDrivingDataPipeline)

# 3. 指定全局 C++ 标准为 C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 4. 获取 examples 目录下所有的 .cpp 文件
file(GLOB EXAMPLES_SRCS "examples/*.cpp")

# 5. 循环遍历每个 .cpp 文件，为每个文件生成一个可执行程序
foreach(SRC_FILE ${EXAMPLES_SRCS})
    # 提取文件名 (不带后缀)，比如把 examples/01_pointers.cpp 提取为 01_pointers
    get_filename_component(TARGET_NAME ${SRC_FILE} NAME_WE)
    
    # 告诉 CMake：我要编译一个叫 TARGET_NAME 的程序，源码是 SRC_FILE
    add_executable(${TARGET_NAME} ${SRC_FILE})
    
    # 针对多线程相关的代码（09_multithreading_basic, 10_mutex_and_locks），
    # 在 Linux 下必须链接 pthread 库。这里为所有目标都链接 pthread 保证安全。
    target_link_libraries(${TARGET_NAME} PRIVATE pthread)
endforeach()
