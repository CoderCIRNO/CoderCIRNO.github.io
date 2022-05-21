# Tips

- **负数的右移位操作**

C++中右移操作默认是算数右移，对于负数，右移会保留符号，使用时需要格外注意。

- **默认拷贝构造**

默认拷贝构造是完全复制目标的那一段内存，因此如果一个结构体中包含一个数组——那么它在结构体的默认拷贝构造中会产生一份新的副本。

但如果包含的是一个指针，则只是浅拷贝，也就是复制一个指向同一片内存的指针。要格外注意对此是否需要做深拷贝处理。