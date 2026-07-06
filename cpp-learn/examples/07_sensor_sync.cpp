/**
 * 实战项目 3：多传感器时间戳同步
 * 
 * 场景：相机频率 30Hz，雷达频率 10Hz。当相机拍到一张照片时，我们需要
 *      在雷达数据流中，找到离这个相机时间戳“最近”的一帧雷达数据。
 * 
 * 学习点：std::map (红黑树)、算法复杂度优化、二分查找 lower_bound
 */

#include <iostream>
#include <map>
#include <string>
#include <cmath>

// 模拟雷达数据
struct RadarData {
    std::string point_cloud_id;
    int object_count;
};

int main() {
    std::cout << "=== 项目3：多传感器时间戳同步 (std::map 查找) ===\n\n";

    // 1. std::map 底层是红黑树，插入时会自动按照 key (这里是时间戳) 从小到大排序
    std::map<uint64_t, RadarData> radar_stream;
    
    // 模拟写入雷达数据 (乱序插入，map 会自动排序)
    radar_stream[10050] = {"PCD_002", 5};
    radar_stream[10000] = {"PCD_001", 3};
    radar_stream[10100] = {"PCD_003", 8};
    radar_stream[10200] = {"PCD_004", 2};
    
    std::cout << "   [雷达流] 当前雷达数据已就绪 (Map自动排序)。\n";

    // 2. 假设相机的某个时间戳
    uint64_t camera_timestamp = 10060;
    std::cout << "   [相机请求] 寻找最接近时间戳: " << camera_timestamp << " 的雷达帧\n";

    // 3. 核心算法：使用 lower_bound 进行 $O(\log n)$ 二分查找
    // lower_bound 返回第一个 "大于等于" camera_timestamp 的迭代器
    auto it = radar_stream.lower_bound(camera_timestamp);

    // 开始判断最近的是哪一帧
    if (it == radar_stream.end()) {
        // 如果迭代器到了末尾，说明请求的时间比雷达流里所有的都晚，直接取最后一帧
        --it;
        std::cout << "   找到匹配: " << it->second.point_cloud_id 
                  << " (时间戳: " << it->first << ")\n";
    } else if (it == radar_stream.begin()) {
        // 如果是第一帧，说明请求的时间比雷达流所有的都早，直接取第一帧
        std::cout << "   找到匹配: " << it->second.point_cloud_id 
                  << " (时间戳: " << it->first << ")\n";
    } else {
        // 关键逻辑：请求时间卡在两个雷达帧中间，我们需要比较前一帧和当前帧哪个更近
        auto prev_it = it;
        --prev_it; // 拿到前一帧

        // 计算时间差
        uint64_t diff_next = it->first - camera_timestamp;
        uint64_t diff_prev = camera_timestamp - prev_it->first;

        // 选时间差更小的那一帧
        auto best_it = (diff_prev <= diff_next) ? prev_it : it;

        std::cout << "   经过前后比对，找到最匹配雷达帧: " << best_it->second.point_cloud_id 
                  << " (时间戳: " << best_it->first << ")\n";
        std::cout << "   (与相机的时间误差为 " << std::min(diff_prev, diff_next) << " 毫秒)\n";
    }

    return 0;
}
