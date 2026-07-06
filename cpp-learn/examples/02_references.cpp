/**
 * 第二课：引用 (References)
 *
 * 引用 = 已有变量的别名, 必须初始化, 不能重新绑定
 * 语法: 类型& 引用名 = 变量;
 */

#include <iostream>
#include <string>

void swap_by_reference(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

void print_value(int val) {
    std::cout << "   值传递: val = " << val << "\n";
}

void print_reference(const int& val) {
    std::cout << "   引用传递: val = " << val << " (避免拷贝)\n";
}

int main() {
    std::cout << "=== C++ 引用学习 ===\n\n";

    // 1. 基本引用
    int x = 42;
    int& ref = x;  // ref 是 x 的别名

    std::cout << "1. 基本操作\n";
    std::cout << "   x = " << x << ", ref = " << ref << "\n";
    ref = 100;
    std::cout << "   修改 ref 后, x = " << x << " (原变量也变了)\n\n";

    // 2. 引用 vs 指针
    std::cout << "2. 引用 vs 指针\n";
    std::cout << "   引用: 必须初始化, 不能为 null, 语法更简洁\n";
    std::cout << "   指针: 可以为 null, 可以重新指向, 需要 * 解引用\n\n";

    // 3. const 引用 (常用作函数参数, 避免拷贝且防止修改)
    const int& const_ref = x;
    std::cout << "3. const 引用\n";
    std::cout << "   const_ref = " << const_ref << "\n";
    // const_ref = 200;  // 编译错误: 不能通过 const 引用修改

    // 4. 引用与函数参数
    std::cout << "\n4. 函数参数传递方式\n";
    int num = 42;
    print_value(num);
    print_reference(num);

    // 5. 引用交换
    int a = 5, b = 10;
    std::cout << "\n5. 用引用交换: 交换前 a=" << a << ", b=" << b << "\n";
    swap_by_reference(a, b);
    std::cout << "   交换后 a=" << a << ", b=" << b << "\n\n";

    // 6. 引用与范围 for
    std::cout << "6. 范围 for 中使用引用避免拷贝\n";
    std::string words[] = {"hello", "world", "cpp"};
    for (const std::string& word : words) {
        std::cout << "   " << word << "\n";
    }

    // 7. 左值引用 vs 右值引用 (C++11)
    std::cout << "\n7. 右值引用 (C++11 move 语义基础)\n";
    int&& rref = 42;  // 绑定到临时值(右值)
    std::cout << "   int&& rref = 42, rref = " << rref << "\n";

    return 0;
}
