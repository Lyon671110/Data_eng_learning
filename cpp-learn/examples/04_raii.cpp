/**
 * 第四课：RAII 资源管理
 *
 * RAII = Resource Acquisition Is Initialization
 *      资源获取即初始化
 *
 * 核心思想: 在构造函数里获取资源, 在析构函数里自动释放
 * 离开作用域时, 对象销毁 -> 资源自动归还, 不用手写 delete/close
 */

#include <fstream>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>

// ========== 1. 反面例子: 手动管理容易出错 ==========
void bad_example() {
    int* p = new int(42);
    // 如果中间 return 或抛异常, 下面的 delete 可能执行不到 -> 内存泄漏
    if (*p > 100) {
        return;  // 泄漏!
    }
    delete p;
}

// ========== 2. 自定义 RAII 类: 文件守卫 ==========
class FileGuard {
public:
    explicit FileGuard(const std::string& path)
        : path_(path), file_(path) {
        if (file_) {
            std::cout << "   [FileGuard] 打开: " << path_ << "\n";
        }
    }

    ~FileGuard() {
        if (file_.is_open()) {
            file_.close();
        }
        std::cout << "   [FileGuard] 自动关闭: " << path_ << "\n";
    }

    // 禁止拷贝, 避免两个对象关同一个文件
    FileGuard(const FileGuard&) = delete;
    FileGuard& operator=(const FileGuard&) = delete;

    std::ifstream& get() { return file_; }
    explicit operator bool() const { return static_cast<bool>(file_); }

private:
    std::string path_;
    std::ifstream file_;
};

// ========== 3. 自定义 RAII 类: 计数器 (演示析构时机) ==========
class ScopeTracer {
public:
    explicit ScopeTracer(std::string name) : name_(std::move(name)) {
        std::cout << "   [ScopeTracer] 进入: " << name_ << "\n";
    }
    ~ScopeTracer() {
        std::cout << "   [ScopeTracer] 离开: " << name_ << " (自动清理)\n";
    }

private:
    std::string name_;
};

// ========== 4. 用 unique_ptr 做 RAII (堆内存) ==========
void use_unique_ptr() {
    auto data = std::make_unique<int[]>(4);
    data[0] = 10;
    data[1] = 20;
    std::cout << "   unique_ptr 数组: " << data[0] << ", " << data[1] << "\n";
    // 函数结束, 自动 delete[]
}

// ========== 5. lock_guard: 标准库的 RAII 锁 ==========
std::mutex g_mutex;
int g_counter = 0;

void increment_with_lock() {
    std::lock_guard<std::mutex> lock(g_mutex);  // 构造时加锁
    ++g_counter;
    // 析构时自动 unlock, 即使中间 return 也安全
}

int main() {
    std::cout << "=== C++ RAII 资源管理 ===\n\n";

    // 1. 作用域结束 -> 析构函数自动调用
    std::cout << "1. 作用域与析构\n";
    {
        ScopeTracer block("内层代码块");
        std::cout << "   正在执行...\n";
    }  // block 在这里销毁, 自动打印 "离开"
    std::cout << "\n";

    // 2. 文件 RAII: 不用手写 close
    std::cout << "2. FileGuard 自动关文件\n";
    {
        FileGuard input("examples/data.txt");
        if (input) {
            std::string line;
            int line_no = 0;
            while (std::getline(input.get(), line)) {
                std::cout << "   第" << ++line_no << "行: " << line << "\n";
            }
        }
    }  // input 析构, 文件自动关闭
    std::cout << "\n";

    // 3. unique_ptr 也是 RAII
    std::cout << "3. unique_ptr (堆内存 RAII)\n";
    use_unique_ptr();
    std::cout << "   use_unique_ptr 返回, 内存已自动释放\n\n";

    // 4. lock_guard 也是 RAII
    std::cout << "4. lock_guard (互斥锁 RAII)\n";
    increment_with_lock();
    increment_with_lock();
    std::cout << "   g_counter = " << g_counter << " (锁已自动释放)\n\n";

    // 5. 对比总结
    std::cout << "5. RAII 要点\n";
    std::cout << "   - 资源在构造函数中获取\n";
    std::cout << "   - 资源在析构函数中释放\n";
    std::cout << "   - 离开作用域 = 自动清理, 异常也安全\n";
    std::cout << "   - unique_ptr / lock_guard / fstream 都是 RAII\n";

    return 0;
}
