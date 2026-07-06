/**
 * 实战项目 6：互斥与锁 (std::mutex)
 * 
 * 场景：多个传感器线程同时往一个云端“数据缓冲队列 (std::vector)”里塞数据。
 *      如果不加锁，两个线程同时往 vector 里 push_back 会导致内存错乱甚至崩溃（Segmentation Fault）。
 * 
 * 学习点：资源竞争、std::mutex (互斥量)、std::lock_guard (RAII自动加解锁)
 */

#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

// 这是一个全局的共享资源 (临界区)
std::vector<std::string> global_data_queue;

// 保护 global_data_queue 的互斥锁
std::mutex queue_mutex;

// 模拟传感器不断产生数据并写入队列
void sensor_producer(const std::string& sensor_name, int data_count) {
    for (int i = 1; i <= data_count; ++i) {
        // 模拟传感器采集数据需要一点时间
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        
        std::string data_packet = sensor_name + "_Frame_" + std::to_string(i);

        // ==========================================
        // 【关键区】加锁保护：确保同一时刻只有一个线程能操作 vector
        // ==========================================
        {
            // std::lock_guard 是 RAII 的体现（上节课学过）
            // 构造时自动加锁 (lock)，离开大括号作用域时自动解锁 (unlock)
            std::lock_guard<std::mutex> lock(queue_mutex);
            
            global_data_queue.push_back(data_packet);
            std::cout << "[" << sensor_name << "] 写入了数据: " << data_packet << "\n";
            
        } // <- 在这里自动解锁，允许其他线程抢锁
    }
}

int main() {
    std::cout << "=== 项目6：互斥锁保护线程安全的缓冲队列 ===\n\n";

    // 启动三个传感器线程，它们会疯狂地向同一个 vector 抢占写入
    std::thread t1(sensor_producer, "Camera", 5);
    std::thread t2(sensor_producer, "LiDAR", 10);
    std::thread t3(sensor_producer, "GPS", 7);

    // 等待所有传感器写完
    t1.join();
    t2.join();
    t3.join();

    std::cout << "\n[Main Thread] 所有传感器停止写入。\n";
    std::cout << "队列中总共收集到 " << global_data_queue.size() << " 帧数据。\n";
    
    // 因为这里所有子线程已经结束，没有竞争了，所以不用加锁就能安全遍历
    std::cout << "\n前5帧数据预览:\n";
    for (int i = 0; i < 5 && i < (int)global_data_queue.size(); ++i) {
        std::cout << "  " << global_data_queue[i] << "\n";
    }

    return 0;
}
