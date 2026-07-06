/**
 * 第一课：指针 (Pointers)
 *
 * 指针 = 存储另一个变量内存地址的变量
 * 语法: 类型* 指针名;
 */

#include <iostream>
#include <memory>

void swap_by_pointer(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    std::cout << "=== C++ 指针学习 ===\n\n";

    // 1. 声明与初始化
    int x = 42;
    int* ptr = &x;  // ptr 指向 x 的地址

    std::cout << "1. 基本操作\n";
    std::cout << "   x 的值:     " << x << "\n";
    std::cout << "   x 的地址:   " << &x << "\n";
    std::cout << "   ptr 存的地址: " << ptr << "\n";
    std::cout << "   *ptr (解引用): " << *ptr << "\n\n";

    // 2. 通过指针修改值
    *ptr = 100;
    std::cout << "2. 通过指针修改后, x = " << x << "\n\n";

    // 3. 空指针
    int* null_ptr = nullptr;
    std::cout << "3. 空指针 nullptr, 使用前必须检查\n";
    if (null_ptr != nullptr) {
        std::cout << *null_ptr;
    } else {
        std::cout << "   null_ptr 是空的, 不能解引用\n\n";
    }

    // 4. 指针与数组
    int arr[] = {10, 20, 30, 40, 50};
    int* arr_ptr = arr;  // 数组名即首元素地址
   
    std::cout << "4. 指针遍历数组\n";
    for (int i = 0; i < 5; ++i) {
        std::cout << "   arr[" << i << "] = " << arr_ptr[i] << "\n";
    }
    std::cout << "\n";

    // 5. 指针作为函数参数
    int a = 5, b = 10;
    std::cout << "5. 用指针交换: 交换前 a=" << a << ", b=" << b << "\n";
    swap_by_pointer(&a, &b);
    std::cout << "   交换后 a=" << a << ", b=" << b << "\n\n";

    // 6. 动态内存: 优先用 unique_ptr (自动释放, 无需手写 delete)
    // 旧写法: int* p = new int(99); ... delete p; p = nullptr;
    std::cout << "6. 动态内存 (unique_ptr)\n";
    auto dynamic = std::make_unique<int>(99);
    std::cout << "   make_unique<int>(99) -> *dynamic = " << *dynamic << "\n";
    *dynamic = 200;
    std::cout << "   修改后 *dynamic = " << *dynamic << "\n";
    std::cout << "   离开作用域时自动释放, 无需 delete\n";

  

    int c[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int* p = c;
    for (int i = 0; i<10; i++) {
        std::cout << "i = " << *(p+i) << "\n";
    }
    return 0;
}
