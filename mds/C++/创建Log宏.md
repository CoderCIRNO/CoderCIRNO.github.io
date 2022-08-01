# 创建Log宏

可以通过以下代码创建Log宏（仿照Qcom offline log）

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