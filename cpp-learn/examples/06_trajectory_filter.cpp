/**
 * 实战项目 2：场景挖掘中的轨迹清洗
 * 
 * 场景：你得到了一段车辆轨迹数据（坐标和速度），需要过滤掉速度异常的噪点，
 *      并计算清洗后的平均速度。同时需要用 RAII 记录处理日志。
 * 
 * 学习点：引用传递(避免大数据拷贝)、RAII(安全管理日志文件)、循环与数学计算
 */

#include <iostream>
#include <vector>
#include <fstream>
#include <string>

// 1. 定义轨迹点结构体
struct TrajectoryPoint {
    double x;
    double y;
    double velocity; // 速度 (m/s)
};

// 2. 简单的 RAII 日志类 (类似之前的 FileGuard)
class Logger {
public:
    explicit Logger(const std::string& filename) : file_(filename) {
        if (file_) {
            file_ << "[开始处理] 日志初始化成功。\n";
        }
    }
    ~Logger() {
        if (file_) {
            file_ << "[结束处理] 日志自动安全关闭。\n";
            file_.close();
        }
    }
    // 禁止拷贝
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    // 提供一个写入日志的接口
    void log(const std::string& msg) {
        if (file_) {
            file_ << msg << "\n";
        }
    }
private:
    std::ofstream file_;
};

// 3. 清洗函数：注意这里参数是 std::vector<TrajectoryPoint>& traj
// 使用 & (引用) 表示直接在原数据上修改，避免了拷贝整个大数组
void filter_noise(std::vector<TrajectoryPoint>& traj, Logger& logger) {
    std::vector<TrajectoryPoint> clean_traj;
    double speed_limit = 40.0; // 假设速度大于 40m/s (144km/h) 是传感器噪点

    for (const auto& pt : traj) { // 使用 const auto& 避免拷贝每个点
        if (pt.velocity <= speed_limit) {
            clean_traj.push_back(pt);
        } else {
            logger.log("过滤异常噪点: 速度 " + std::to_string(pt.velocity) + " m/s");
        }
    }

    // 打印过滤掉的数量
    std::cout << "   [清洗] 过滤掉了 " << (traj.size() - clean_traj.size()) << " 个噪点。\n";
    
    // 把清洗后的结果替换掉原来的
    traj = std::move(clean_traj); 
}

int main() {
    std::cout << "=== 项目2：轨迹数据清洗与 RAII 日志 ===\n\n";

    // 模拟一段轨迹数据 (包含正常点和噪点)
    std::vector<TrajectoryPoint> my_trajectory = {
        {0.0, 0.0, 15.2},
        {1.0, 1.2, 15.8},
        {2.0, 2.5, 99.9}, // 异常噪点！
        {3.0, 3.7, 16.1},
        {4.0, 5.0, 120.5} // 异常噪点！
    };

    std::cout << "   清洗前数据量: " << my_trajectory.size() << "\n";

    // 利用作用域 {} 来控制 Logger 的生命周期
    {
        Logger my_logger("build/clean_log.txt");
        
        // 调用清洗函数，传入引用
        filter_noise(my_trajectory, my_logger);

        // 计算平均速度
        double sum_velocity = 0;
        for (const auto& pt : my_trajectory) {
            sum_velocity += pt.velocity;
        }
        double avg_velocity = my_trajectory.empty() ? 0 : sum_velocity / my_trajectory.size();
        
        my_logger.log("清洗完成，平均速度: " + std::to_string(avg_velocity) + " m/s");
        std::cout << "   清洗后数据量: " << my_trajectory.size() << "\n";
        std::cout << "   计算出平均速度: " << avg_velocity << " m/s\n";
        std::cout << "   (日志已写入 build/clean_log.txt)\n";
    } // 离开作用域，my_logger 会自动调用析构函数，关闭并保存日志文件

    return 0;
}
