# float精度问题

阅读此代码

```cpp
#include<iostream>
using namespace std;

int main(void){
    if(0.1 + 0.2 == 0.3){
        cout<<"eq"<<endl;
    }else{
        cout<<"!eq"<<endl;
    }
}
```

如果只运用数学常识进行判断，可以推测代码会输出的是eq；然而实际上由于浮点数精度问题（与浮点数的存储方式有关），实际上会输出的是!eq。

如果坚持要进行这种判断，只能进行一个近似操作：

```cpp
#include<iostream>
#include<cmath>
using namespace std;

int main(void){
    if(abs((0.1 + 0.2) - 0.3) < 0.0001){
        cout<<"eq"<<endl;
    }else{
        cout<<"!eq"<<endl;
    }
}
```

其中的0.0001可根据需要的精度调整。
