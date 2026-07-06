/**
 * 实战项目 5：多线程基础 (std::thread)
 * 
 * 场景：数据入库时，我们需要同时解压并处理“相机图像”和“雷达点云”。
 *      如果串行处理会很慢，我们使用多线程让它们同时进行。
 * 
 * 学习点：std::thread 的创建、std::chrono(时间控制)、join(等待线程结束)
 */

#include <iostream>
#include <thread>
#include <chrono>

// 模拟处理相机图像的耗时任务
void process_camera_data() {
    std::cout << "[Camera Thread] 开始解码相机 H265 视频流...\n";
    // 模拟耗时 800 毫秒
    std::this_thread::sleep_for(std::chrono::milliseconds(800));
    std::cout << "[Camera Thread] 相机视频流解码完成！\n";
}

// 模拟处理雷达点云的耗时任务
void process_lidar_data() {
    std::cout << "[LiDAR Thread] 开始解析激光雷达 PCD 点云...\n";
    // 模拟耗时 1200 毫秒
    std::this_thread::sleep_for(std::chrono::milliseconds(1200));
    std::cout << "[LiDAR Thread] 雷达点云解析完成！\n";
}

int main() {
    std::cout << "=== 项目5：多线程并发处理传感器数据 ===\n\n";

    auto start_time = std::chrono::steady_clock::now();

    // 1. 创建并启动线程
    // 此时主线程会继续往下走，而 t1 和 t2 会在后台同时跑
    std::thread t1(process_camera_data);
    std::thread t2(process_lidar_data);

    std::cout << "[Main Thread] 已经派发了相机和雷达的处理任务，主线程可以干点别的...\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    std::cout << "[Main Thread] 主线程干完了自己的事，等待子线程结束...\n";

    // 2. 阻塞主线程，等待子线程完成 (必须调用 join 或 detach)
    // 如果不 join，主线程(main)一结束，子线程会被强行杀掉，程序会崩溃 (std::terminate)
    t1.join(); 
    t2.join();

    auto end_time = std::chrono::steady_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

    std::cout << "\n[Main Thread] 所有数据处理完毕！\n";
    std::cout << "总耗时: " << diff.count() << " 毫秒 (并行处理，总耗时接近于最慢的那个任务)\n";

    return 0;
}
