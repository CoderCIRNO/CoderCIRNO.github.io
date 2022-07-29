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

`const`成员函数不能调用`non-const`成员函数，反之则可以。

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

## 条款04

### 一个规则

确保每一个构造函数都将对象的每一个成员初始化。

### 关于成员初值列

[跳转链接](../%E6%88%90%E5%91%98%E5%88%9D%E5%80%BC%E5%88%97%E7%9A%84%E6%95%88%E7%8E%87%E4%BC%98%E5%8A%BF.html)

### non-local static

不同编译单元中定义的`non-local static`对象，其初始化顺序无法确定（`static`对象在其声明代码首次被加载到内存中时，被初始化，即我们无法确定不同编译单元中代码的加载顺序）。不过我们可以把这种对象放在其专属函数内，让这个函数返回其引用。参考[编译时初始化](../%E7%BC%96%E8%AF%91%E6%97%B6%E5%88%9D%E5%A7%8B%E5%8C%96.html)。

且从C++11起，这一做法就已经可以保证多线程安全。

## 条款05

### 空类

编译器会为一个空类生成默认构造函数、拷贝构造、`operator=`操作符和一个析构函数，如果开发者特意为一个类声明这其中的某个函数，那么此默认函数将不再被自动生成。

### 默认的拷贝构造

其功能是将来源对象的每一个non-static成员变量拷贝到目标对象，即所谓浅拷贝。

但如果成员变量中含有引用，则默认拷贝构造不会被生成，因为C++并不允许改变引用的指向。如果开发者没有为其定义拷贝构造，那么这个类将不存在拷贝构造函数，任何对象间的copy操作都无法通过编译。

## 条款07

### 纯虚函数

有时需要一个完全抽象类，但手头没有纯虚函数的需求，这种情况下可以将它的析构声明为纯虚函数，不过必须为这个纯虚析构提供一份定义，否则无法通过编译。

## 条款08

### 如果析构可能会发生异常

单独拿出析构函数中可能存在风险的部分，并给类设置双重保险：

```cpp
class DBConn{
public:
    void close()
    {
        db.close();
        closed = true;
    }
    ~DBConn()
    {
        if (!closed)
        {
            try {
                db.close();
            }
            catch (...) {
                //记录异常，结束程序或直接吞下异常
            }
        }
    }
private:
    DBConnection db;
    bool closed;
};
```

这种设计给了客户一个防范风险的机会，能让他们提前处理错误。而且即便客户忽略了这个机会，也不会引入额外的风险。

**[TBC]**

## 条款30

### inline的缺点

- 增大程序体积，在内存有限的机器上慎用（嵌入式）。

- 造成代码膨胀，导致额外的换页行为，降低高速缓存hit率，有时甚至导致负优化。

- 更新`inline`函数时，所有使用此代码的文件都需要重新编译。

- 增大调试难度（懂的都懂）。

### inline是一个申请，而不是要求

`inline`关键字是一个申请，具体是否在编译期展开，最终由编译器来决定。如果使用`-O0`参数来编译，则任何`inline`函数都不会被展开。

即便编译器认为某个函数应当被内联，如果此函数在某处被取地址，编译器还是会为它生成一个函数本体。当通过指针调用时，使用正常调用。当通过函数名调用时，编译器会内联处理。

## 条款33

### 关于变量名称遮蔽

同个作用域下不能声明两个同名变量，但只要作用域不同，就可以声明同名变量，编译器在寻找变量时，先在较小的作用域中寻找，如果没有，再层层向上寻找外部作用域。

```cpp
int a = 0;

int main(void){
    int a = 1;
    {
        int a = 2;
        cout<<a<<endl; // 输出"2"
        {
            char a = 'H';
            cout<<a<<endl; // 输出"H"
        }
    }
    cout<<a<<endl; //输出 "1"
}
```

*ps: 小米禁止shadow变量(`-Werror`,`-Wshadow`)*

## 条款37

### 缺省值静态绑定

以下代码：

```cpp
class Base
{
public:
    virtual void test(int output0 = 1)
    {
        cout<<"B:"<<output0<<endl;
    }
};

class Derived:public Base
{
public:
    virtual void test(int output1 = 2)
    {
        cout<<"D:"<<output1<<endl;
    }
};

int main(void){
    Derived D;
    D.test(); //D:2
    Base *pD = new Derived;
    pD->test(); //D:1
}
```

观察代码基本可以认定，在使用缺省参数调用`Derived`类的`test()`函数时，其输出固定为"D:2"，然而事实并非如此：

`D.test()`输出为"D:2"，符合预期。

`pD->test()`实际输出为"D:1"，程序确实调用到了`Derived::test`，但却使用了`Base::test`的缺省参数，这种组合几乎很难被预测。

出现这种现象的原因是：虚函数动态绑定，而缺省参数静态绑定（不知出于何种考量，缺省参数是在编译期就被确定下来的）。在调用`pD->test()`前，根据缺省参数静态绑定，`Base::test`的缺省参数`1`被放入寄存器，在实际`call`函数时，根据动态绑定，程序去虚函数表中找到了应该调用的`Derived::test`，于是自然产生了这种结果。

接下来再考虑另一情况：如果`Derived::test`和`Base::test`的缺省参数类型不同，乃至个数不同呢？

```cpp
class Base
{
public:
    virtual void test(char output0 = 'A') //char
    {
        cout<<"B:"<<output0<<endl;
    }
};

class Derived:public Base
{
public:
    virtual void test(int output1 = 2) //int
    {
        cout<<"D:"<<output1<<endl;
    }
};

int main(void){
    Derived D;
    D.test(); //D:2
    Base *pD = new Derived;
    pD->test(); //B:A
}
```

如果真的出现了这种情况，很遗憾，通过`Base`类型指针是再也不可能调用到`Derived::test`了，不论它指向谁，无论我们给它怎样的参数，就好像我们从没定义过`Derived::test`一样，并且编译器对此不会给出任何提示，除非是给`Base::test`传入了“错误的”参数类型或个数。

实际上编译器在处理这种情况时，做了这样的处理：`Base::test`和`Derived::test`都被放进了`Derived`类的虚函数表里，在调用时根据指针的类型决定调用哪个函数，这像是一个`non-virtual`的`virtual`函数——它确实在虚函数表里，却要根据指针类型来调用。

```
; static_cast<Base*>(pD)->test()
 mov    rax,QWORD PTR [rbp-0x18]
 mov    rax,QWORD PTR [rax]
 mov    rdx,QWORD PTR [rax]
 mov    rax,QWORD PTR [rbp-0x18]
 mov    esi,0x41
 mov    rdi,rax
 call   rdx

; static_cast<Derived*>(pD)->test()
; 如果pD指向一个Base对象，会发生段错误
 mov    rax,QWORD PTR [rbp-0x18]
 mov    rax,QWORD PTR [rax]
 add    rax,0x8
 mov    rdx,QWORD PTR [rax]
 mov    rax,QWORD PTR [rbp-0x18]
 mov    esi,0x2
 mov    rdi,rax
 call   rdx
```

总之：

尽量不要给虚函数设置缺省参数，在非设不可时，考虑使用`non-virtual`接口。

**[TBC]**