/**
 * 第五课实战：极简版自动驾驶数据解析器
 * 
 * 场景：车端记录了传感器数据的二进制文件，但由于多线程写入，
 *      时间戳可能是乱序的。我们需要读取它并按时间顺序排好。
 * 
 * 学习点：结构体(struct)、二进制读写(fstream)、vector、自定义排序(sort)
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cstdint> // 为了使用明确位数的类型如 uint64_t

// 1. 定义数据结构：传感器数据头
struct SensorData {
    uint64_t timestamp; // 时间戳 (微秒)
    uint32_t sensor_id; // 传感器ID (比如 0:前视相机, 1:激光雷达)
    uint32_t data_size; // 数据大小 (字节)
};

// 辅助函数：生成一个模拟的、乱序的二进制数据文件
void generate_mock_bag(const std::string& filename) {
    std::ofstream out(filename, std::ios::binary);
    if (!out) {
        std::cerr << "无法创建模拟文件!\n";
        return;
    }

    // 故意打乱时间戳顺序
    std::vector<SensorData> mock_data = {
        {1627890005000, 1, 45000}, // LiDAR
        {1627890001000, 0, 102400}, // Camera (最早的)
        {1627890003000, 0, 103000}, // Camera
        {1627890008000, 1, 46000}  // LiDAR (最晚的)
    };

    // 把 vector 里的数据直接按二进制写到文件里
    for (const auto& data : mock_data) {
        // 强转指针为 char* 写入
        out.write(reinterpret_cast<const char*>(&data), sizeof(SensorData));
    }
    out.close();
    std::cout << "[车端模拟] 已生成乱序的二进制数据文件: " << filename << "\n\n";
}

int main() {
    std::cout << "=== 自动驾驶数据闭环: 解析与时间戳排序 ===\n\n";

    std::string bag_file = "build/mock_bag.bin";
    
    // 步骤 A: 生成测试文件
    generate_mock_bag(bag_file);

    // 步骤 B: 云端开始解析二进制文件
    std::cout << "[云端处理] 开始解析...\n";
    std::ifstream in(bag_file, std::ios::binary);
    if (!in) {
        std::cerr << "文件打开失败!\n";
        return 1;
    }

    std::vector<SensorData> parsed_data;
    SensorData temp;

    // 每次从文件里读取 sizeof(SensorData) 大小的数据，放到 temp 中
    while (in.read(reinterpret_cast<char*>(&temp), sizeof(SensorData))) {
        parsed_data.push_back(temp); // 存入 vector
    }
    in.close();

    std::cout << "   共解析出 " << parsed_data.size() << " 帧数据。\n";
    std::cout << "   排序前:\n";
    for (const auto& d : parsed_data) {
        std::cout << "     时间戳: " << d.timestamp 
                  << " | 传感器: " << d.sensor_id 
                  << " | 大小: " << d.data_size << "\n";
    }

    // 步骤 C: 按照时间戳排序 (使用 C++11 的 lambda 表达式自定义排序规则)
    std::sort(parsed_data.begin(), parsed_data.end(), 
        // 这里的 [](const SensorData& a, const SensorData& b) 就是告诉 sort 如何比较两个元素
        [](const SensorData& a, const SensorData& b) {
            return a.timestamp < b.timestamp; // 时间戳小的排前面
        }
    );

    std::cout << "\n   排序后:\n";
    for (const auto& d : parsed_data) {
        std::cout << "     时间戳: " << d.timestamp 
                  << " | 传感器: " << d.sensor_id 
                  << " | 大小: " << d.data_size << "\n";
    }

    return 0;
}
