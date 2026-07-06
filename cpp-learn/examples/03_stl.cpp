/**
 * 第三课：STL 标准模板库
 *
 * 常用容器: vector, map, set, string
 * 常用算法: sort, find, count
 */

#include <algorithm>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <fstream>

int main() {
    std::cout << "=== C++ STL 学习 ===\n\n";

    // ========== 1. vector 动态数组 ==========
    std::cout << "1. vector (动态数组)\n";
    std::vector<int> nums = {3, 1, 4, 1, 5, 9};

    nums.push_back(2);
    nums.push_back(6);

    std::cout << "   元素: ";
    for (int n : nums) {
        std::cout << n << " ";
    }
    std::cout << "\n   size=" << nums.size() << ", capacity=" << nums.capacity() << "\n";

    std::sort(nums.begin(), nums.end());
    
    std::cout << "   排序后: ";
    for (int n : nums) {
        std::cout << n << " ";
    }
    std::cout << "\n\n";

    // ========== 2. string ==========
    std::cout << "2. string\n";
    std::string s = "Hello";
    s += " C++";
    std::cout << "   s = \"" << s << "\"\n";
    std::cout << "   length = " << s.length() << "\n";
    std::cout << "   substr(0,5) = \"" << s.substr(0, 5) << "\"\n\n";

    // ========== 3. map 键值对 ==========
    std::cout << "3. map (键值对, 自动按 key 排序)\n";
    std::map<std::string, int> scores;
    scores["Alice"] = 95;
    scores["Bob"] = 87;
    scores["Charlie"] = 92;

    for (const auto& [name, score] : scores) {
        std::cout << "   " << name << ": " << score << "\n";
    }
    std::cout << "   scores[\"Alice\"] = " << scores["Alice"] << "\n\n";

    // ========== 4. set 有序集合 ==========
    std::cout << "4. set (有序, 不重复)\n";
    std::set<int> unique_nums = {3, 1, 4, 1, 5, 9, 2, 6};
    std::cout << "   元素 (自动去重排序): ";
    for (int n : unique_nums) {
        std::cout << n << " ";
    }
    std::cout << "\n\n";

    // ========== 5. 迭代器 ==========
    std::cout << "5. 迭代器\n";
    std::vector<int> v = {10, 20, 30};
    std::cout << "   正向: ";
    for (auto it = v.begin(); it != v.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n   反向: ";
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n\n";

    // ========== 6. 算法 ==========
    std::cout << "6. 算法 (algorithm)\n";
    std::vector<int> data = {5, 2, 8, 2, 1};
    auto it = std::find(data.begin(), data.end(), 8);
    if (it != data.end()) {
        std::cout << "   find(8): 找到, 位置 index=" << (it - data.begin()) << "\n";
    }
    int cnt = std::count(data.begin(), data.end(), 2);
    std::cout << "   count(2): " << cnt << " 个\n";


    std::ifstream in("examples/data.txt");
    std::string line;
    int count = 0;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
        count++;
    }
    std::ofstream out("examples/output.txt");
    out << "count: " << count << "\n";
    out.close();

    return 0;
}
