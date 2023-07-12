# 创建Log宏

## 标准输出

输出到标准输出，并附加开关（在力扣之类需要log调试的场景下非常实用）
```cpp
#define ENABLE_DEBUG 1

#ifdef ENABLE_DEBUG
#define WTLOG(fmt, ...)\
    printf("%s:%d %s()  " fmt "\n", __FILE__, __LINE__, __FUNCTION__, ##__VA_ARGS__);
#else
#define WTLOG(fmt, ...)
#endif
```

## 输出到文件

可以通过以下代码创建Log宏输出到文件（仿照Qcom offline log）

```cpp
#ifndef CAMX_WTLOG
#define CAMX_WTLOG(fmt, ...)\
    {FILE *f_wtl;\
    f_wtl = fopen("/data/vendor/camera/wtlog.txt", "a+");\
    if(NULL != f_wtl){\
        fprintf(f_wtl, "%s:%d %s()  " fmt "\n", __FILE__, __LINE__, __FUNCTION__, ##__VA_ARGS__);\
    }\
    fclose(f_wtl);}
#endif
```

实时查看

```bash
adb root
clear
adb shell tail -f /data/vendor/camera/wtlog.txt
```

**[TODO]**

增加时间