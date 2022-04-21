# CPU时钟周期

```cpp
static __inline__ unsigned long long GetCycleCount(void)
{
    unsigned long long int x;
    __asm__ volatile (".byte 0x0f, 0x31" : "=A" (x));
    return x;
}
```
用于评估运行效率。