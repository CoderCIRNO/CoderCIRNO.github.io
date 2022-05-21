# 《Effective C++》

## 条款02

### 以 const, enum, inline 替换 #define的优点

- **编译时报错容易定位问题**

c++代码编译的过程：预处理 - 编译 - 汇编 - 链接

`#define`仅在预处理期有意义，如果在代码种定义了一个`#define N 100`，那么在编译期，编译器根本见不到N这个符号，也自然不会进到符号表种。

假使这个`N`在编译中引发了某种错误，那么编译器只会提到`"100"`而不是`"N"`，在一些情况下，这种报错很可能会让人摸不到头脑，更有甚者，如果程序员不幸写出了`"N100"`这种代码，编译器甚至会提示问题出在`"100100"`上，这会让报错信息的迷惑性更上一层楼。

而如果用`const int N = 100;`来替代这一功能，编译器就会很明白的提示问题出在`"N"`上。

- **可以提供易处理的作用域与可见性**

`#define`并不重视作用域，一旦被定义，在后续的预处理中就都会被替换，除非使用了`#undef`，如此一来，控制`#define`的作用域会变得相当困难。

并且，`#define`并不提供任何封装性，它对一切可见，这也不符合C++的设计思想。

- **尽量不使用宏函数，能够避免歧义**

宏函数因为没有普通函数传参、入栈出栈、地址跳转之类的开销，而备受推崇，不过在某些情况下，宏函数的特性会非常让人困惑。

```cpp
#define CALL_WTIH_MAX(a, b) f((a) > (b) ? (a) : (b))

int a = 5;
int b = 0;
CALL_WITH_MAX(++a, b);        // a被累加两次
CALL_WITH_MAX(++a, b + 10);   // a被累加一次
```

产生这种歧义的原因在于，`++a`被用于替换了宏函数中的所有`a`，三目运算符中的`a`也如此，因此当`a`比较大时，`++a`被自然的执行了两次————比较时一次，得到结果时，又一次，这大概并不符合这个宏函数的设计初衷。

## 条款03

### const与指针

`const`在和指针搭配时，有三种用法。
```cpp
const int* a;       // 指向的数据不可变，但指针本身可变
int const* a;       // 同上，这两种用法和下一种的区别在于const和*的相对位置
int* const a;       // 指针本身不可变，但指向的数据可变
const int* const a; // 指针本身和其指向的数据都不可变
```
另外，`volatile`关键字修饰指针时与`const`比较相似。

### const与STL迭代器

迭代器是指针的一种封装，声明`iterator`迭代器为const，就和声明`T* const`指针一样，即其本身不可变，但指向的数据可变。

如果想要使用`const T*`，要声明为`const_iteratot`。

### const与函数

一般情况下，`const`成员函数不能修改成员变量，但以`mutable`修饰的成员变量除外。

### 一种减少代码重复量的做法

```cpp
class TB{
public:
    const char& operator[](std::size_t position) const
    {
        // 一些复杂操作，比如记录访问记录、判断是否越界之类…
        return text[position];
    }
    char& operatot[](std::size_t position)
    {
        return const_cast<char&>(
            static_cast<const TextBlock&>(*this)[position]
        );
    }
private:
    char text[256];
};
```
如上，对于`[]`运算符，如果作用于`TextBlock`，则返回可修改的`text`引用；如作用于`const TextBlock`，则返回`const text`引用。

如上的写法能在保证`TextBlock`和`const TextBlock`的`[]`运算符功能的同时，省去重写一遍注释处操作的麻烦。

其弊在于两次转换拉低了效率；其利在于减少了不必要的代码量、还能降低维护成本（如果选择重写一遍，后续变更操作符功能时需要做两次同样的修改，还埋下了只修改一处忘记另一处的风险）。


**[TBC]**