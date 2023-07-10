# sort自定义排序函数实现字典排序

备忘

```cpp
#include<iostream>
#include<stdlib.h>
#include<algorithm>
#include<vector>
#include<queue>
using namespace std;

bool cmp(string a, string b){
  int count = 0;
  const int aSize = a.size();
  const int bSize = b.size();
  while(count < aSize && count < bSize && a[count] == b[count]){
    count++;
  }
  if(count == aSize){
    return 1;
  }else if(count == bSize){
    return 0;
  }else{
    return int(a[count]) < int(b[count]);
  }
}

int main(void){
  vector<string> data = {"abcde", "abcdd", "abc", "ccc", "baa"};
  sort(data.begin(), data.end(), cmp);
  for(string i:data){
    cout<<i<<endl;
  }
  system("pause");
}
```